#!/usr/bin/env python3
"""Generate the ESP Web Tools + ESPHome OTA manifest for a single device.

The manifest format is documented at:
  https://esphome.io/components/update/http_request/

This script is called by the release workflow after firmware has been built
and its MD5 computed. It's deliberately small and stdlib-only so it runs
on any CI image without extra dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_manifest(
    *,
    name: str,
    version: str,
    chip_family: str,
    ota_path: str,
    factory_path: str,
    md5: str,
    release_url: str,
) -> dict:
    """Return the manifest dict for a single device build."""
    return {
        "name": name,
        "version": version,
        # Lets Home Assistant recognise the device for adoption.
        "home_assistant_domain": "esphome",
        # Ask users before wiping on a fresh install so existing
        # provisioning isn't lost by accident.
        "new_install_prompt_erase": False,
        "builds": [
            {
                "chipFamily": chip_family,
                "parts": [
                    # The factory image is a full flash image already
                    # offset-packed by ESPHome — offset 0 is correct.
                    {"path": factory_path, "offset": 0},
                ],
                "ota": {
                    "path": ota_path,
                    "md5": md5,
                    "release_url": release_url,
                    "summary": f"{name} firmware v{version}",
                },
            }
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Product display name")
    parser.add_argument("--version", required=True, help="Semver version, no leading v")
    parser.add_argument("--chip-family", required=True, help="e.g. ESP32-C3")
    parser.add_argument(
        "--ota-path",
        required=True,
        help="Path to the OTA bin, relative to the manifest's URL",
    )
    parser.add_argument(
        "--factory-path",
        required=True,
        help="Path to the factory bin, relative to the manifest's URL",
    )
    parser.add_argument("--md5", required=True, help="MD5 of the OTA binary")
    parser.add_argument("--release-url", required=True, help="GitHub Release URL")
    parser.add_argument("--output", required=True, type=Path, help="Where to write manifest.json")
    args = parser.parse_args()

    manifest = build_manifest(
        name=args.name,
        version=args.version,
        chip_family=args.chip_family,
        ota_path=args.ota_path,
        factory_path=args.factory_path,
        md5=args.md5,
        release_url=args.release_url,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
