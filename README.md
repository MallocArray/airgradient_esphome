# AirGradient ESPHome firmware

Firmware builds for multiple AirGradient devices, each versioned and
released independently. Designed to meet the
[Made for ESPHome](https://esphome.io/guides/made_for_esphome/) program
requirements.

## Supported devices

Every device that ships from this repo is declared in [`devices.yaml`](devices.yaml).
At the time of writing that's:

- **AirGradient ONE** (`airgradient-one`) — ESP32-C3 indoor monitor

Adding a new device is covered in its own section below.

## How a release works

Tags are scoped per device: **`<slug>/v<semver>`**. That means each
device has its own version history, release notes, and manifest URL —
bumping one board never triggers a rebuild of another.

```bash
# Cut a stable release for the ONE
git tag airgradient-one/v1.2.3
git push origin airgradient-one/v1.2.3

# Cut a pre-release (skipped from the Pages manifest, listed as
# pre-release on GitHub so fielded devices ignore it)
git tag airgradient-one/v1.3.0-rc.1
git push origin airgradient-one/v1.3.0-rc.1
```

On each tag push the `Build & Release Firmware` workflow:

1. Parses the slug and version out of the tag, looks the slug up in
   `devices.yaml`, and confirms the YAML's `project.version` matches.
2. Compiles the firmware with ESPHome.
3. Publishes to the `gh-pages` branch under `/<slug>/`:
   - `manifest.json` — what the device's `update.http_request` polls.
   - `firmware/latest/` — overwritten each release; referenced by the manifest.
   - `firmware/<version>/` — immutable copy for anyone pinning.
4. Rebuilds the top-level `index.html` listing every device that has
   a manifest on the site, with ESP Web Tools install buttons.
5. Attaches the binaries and MD5 to a GitHub Release at `<slug>/v<version>`.

Manual builds are also available via the **Run workflow** button on
Actions — pick a device from the dropdown to smoke-test a branch
without cutting a release.

## Published URLs

After the first release, every device has:

```
https://<owner>.github.io/<repo>/                         # landing page
https://<owner>.github.io/<repo>/<slug>/manifest.json     # update manifest
https://<owner>.github.io/<repo>/<slug>/firmware/latest/  # latest binaries
https://<owner>.github.io/<repo>/<slug>/firmware/<ver>/   # pinned version
```

Each device's YAML points its `update.http_request.source` at its own
manifest URL, so firmware is only offered to compatible hardware.

## Adding a new device

1. Add a block to `devices.yaml` with the slug, name, YAML path, chip
   family, and node name.
2. Create `<slug>.yaml` alongside `airgradient-one.yaml`. The easiest
   route is copying the ONE config and editing:
   - `substitutions.name` (must match `node_name` in `devices.yaml`)
   - `substitutions.friendly_name`
   - `esphome.project.name` (unique per device)
   - `update.http_request.source` (point at `/<slug>/manifest.json`)
   - `dashboard_import.package_import_url` (point at the new YAML)
   - The `packages:` block for the new hardware.
3. Open a PR. The `Validate configs` workflow compiles every device in
   `devices.yaml` on every PR, so a broken new device fails fast.
4. After merge, tag the first release: `<slug>/v1.0.0`.

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install .
esphome config airgradient-one.yaml       # validate
esphome compile airgradient-one.yaml      # build
esphome run airgradient-one.yaml          # build + upload (wired or OTA)
```

## Made for ESPHome compliance (per device)

| Requirement | Where it's satisfied |
| --- | --- |
| ESP32 / supported variant | Set per device in its `packages/` board file |
| `project` identification | `esphome.project` in each device's YAML |
| Open-source configuration | this repository |
| User-applied updates | `update.http_request` → per-device `manifest.json` |
| Wi-Fi provisioning (BLE) | `esp32_improv` |
| Wi-Fi provisioning (USB) | `improv_serial` |
| Fallback Wi-Fi AP | `wifi.ap` + `captive_portal` |
| Dashboard adoption | `dashboard_import.package_import_url` |
| No secrets / static IPs | credential fields are commented out |
| IDs on components | every top-level component has an explicit `id:` |

Once a device is releasing green and flashable, open a PR on
<https://github.com/esphome/esphome-devices> to add it to the devices
database, and email `esphome@openhomefoundation.org` linking that PR
to request permission to use the logo.

## Repository layout

```
.
├── devices.yaml                    # registry: one entry per releasable device
├── airgradient-one.yaml            # ESPHome config for the ONE
├── <slug>.yaml                     # (future) ESPHome config for each device
├── packages/                       # shared YAML packages (pull from AirGradient upstream)
├── scripts/
│   ├── build_manifest.py           # writes per-device manifest.json
│   └── build_landing_page.py       # rebuilds the Pages index listing every device
├── pyproject.toml                  # pins esphome + pyyaml
├── .github/workflows/
│   ├── build-firmware.yml          # tag-driven build + release + Pages
│   └── validate.yml                # PR-time config validation, matrixed
└── README.md
```

## Before you push: checklist

- [ ] Replace `yourorg` in every device YAML (three spots each:
      `project.name`, `update.source`, `dashboard_import.package_import_url`).
- [ ] In GitHub repo settings: **Pages → Source: Deploy from a branch**
      → select `gh-pages` / `/ (root)`. (The `gh-pages` branch is
      created by the first successful release run.)
- [ ] Confirm the default branch is `main` (or update the
      `dashboard_import` URLs accordingly).
- [ ] Copy AirGradient's `packages/` into this repo (or adjust
      `!include` paths) so every device YAML compiles standalone.
