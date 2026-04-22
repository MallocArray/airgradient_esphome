#!/usr/bin/env python3
"""Build the GitHub Pages landing page listing every published device.

The source of truth for what *could* be published is `devices.yaml`.
A device only appears on the landing page if its manifest.json is
actually present under site/<slug>/manifest.json — so a device added
to devices.yaml but never released is not advertised.

Run after all per-device files have been staged under `site/`.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

# Imported lazily so --help works without pyyaml installed.
def _load_yaml(path: Path):
    import yaml  # type: ignore
    with path.open() as fh:
        return yaml.safe_load(fh)


TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <script
      type="module"
      src="https://unpkg.com/esp-web-tools@10/dist/web/install-button.js?module"
    ></script>
    <style>
      :root {{ color-scheme: light dark; }}
      body {{
        font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
        max-width: 48rem;
        margin: 3rem auto;
        padding: 0 1rem;
        line-height: 1.55;
      }}
      h1 {{ margin-bottom: 0.25rem; }}
      .subtitle {{ color: #666; margin-top: 0; }}
      .device {{
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1.25rem 0;
      }}
      .device h2 {{ margin-top: 0; }}
      .meta {{
        font-size: 0.9rem;
        color: #666;
        margin: 0.25rem 0 1rem;
      }}
      code {{
        background: rgba(128, 128, 128, 0.15);
        padding: 0.1em 0.35em;
        border-radius: 3px;
      }}
    </style>
  </head>
  <body>
    <h1>{title}</h1>
    <p class="subtitle">
      Firmware built with <a href="https://esphome.io/">ESPHome</a>. Connect a
      device over USB in Chrome or Edge on desktop and click Install. Already
      flashed? Devices poll their manifest every six hours and surface updates
      as a <em>Firmware Update</em> entity in Home Assistant.
    </p>

    {cards}

    <p style="font-size: 0.85rem; color: #888; margin-top: 3rem;">
      Source: <a href="https://github.com/{repo}">github.com/{repo}</a>.
    </p>
  </body>
</html>
"""

CARD = """<div class="device">
  <h2>{name}</h2>
  <p>{description}</p>
  <p class="meta">
    Latest version: <strong>v{version}</strong> &middot;
    Chip: <code>{chip}</code> &middot;
    <a href="{slug}/manifest.json">manifest.json</a> &middot;
    <a href="https://github.com/{repo}/releases/tag/{slug}%2Fv{version}">release notes</a>
  </p>
  <esp-web-install-button manifest="{slug}/manifest.json"></esp-web-install-button>
</div>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--devices-file", required=True, type=Path)
    parser.add_argument(
        "--site-dir",
        required=True,
        type=Path,
        help="Root of the Pages site being assembled",
    )
    parser.add_argument("--repo", required=True, help="owner/repo for footer links")
    parser.add_argument("--title", default="ESPHome firmware")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    registry = _load_yaml(args.devices_file)
    cards: list[str] = []

    for device in registry.get("devices", []):
        slug = device["slug"]
        manifest_path = args.site_dir / slug / "manifest.json"
        if not manifest_path.exists():
            # Device is declared but hasn't been released yet — skip it
            # rather than advertising a dead link.
            print(f"skipping {slug}: no manifest at {manifest_path}", file=sys.stderr)
            continue

        try:
            manifest = json.loads(manifest_path.read_text())
            version = manifest["version"]
        except (json.JSONDecodeError, KeyError) as exc:
            print(f"skipping {slug}: malformed manifest ({exc})", file=sys.stderr)
            continue

        cards.append(
            CARD.format(
                name=html.escape(device["name"]),
                description=html.escape(device.get("description", "")),
                version=html.escape(version),
                chip=html.escape(device["chip_family"]),
                slug=html.escape(slug),
                repo=html.escape(args.repo),
            )
        )

    if not cards:
        cards.append(
            "<p><em>No devices published yet. Push a tag like "
            "<code>airgradient-one/v1.0.0</code> to cut the first release.</em></p>"
        )

    args.output.write_text(
        TEMPLATE.format(
            title=html.escape(args.title),
            cards="\n".join(cards),
            repo=html.escape(args.repo),
        )
    )
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
