# TrueNAS SCALE catalog

This is a fork of [a forked TrueCharts App Catalog archive](https://github.com/v3DJG6GL/truecharts_archive) for TrueNAS SCALE to keep a few apps that I have deployed updated.

## How to change your TrueCharts catalog:
1.  Remove your already old/deprecated TrueCharts catalog: _Apps_ --> _Discover Apps_ --> _Manage Catalogs_ --> _TRUECHARTS_ --> _Delete_ (don't worry, this won't delete any of your already installed applications)
2.  Add this repository as a new Catalog:
    +  _Add Catalog_ --> _Continue_
        - **Catalog Name:** TrueCharts
        - **Repository:** https://github.com/ZhangTianrong/truecharts
        - **Preferred Trains:** incubator, premium, stable, system
        - **Branch:** main
    + Wait for a considerable amount of time for TrueNAS to verify that all charts in the repo are well-formated.

## Apps for which the charts are being maintained:

+ navidrome
+ komga
+ nginx-proxy-manager
+ alist
+ wg-easy
+ tachidesk-docker

### Charts mainted by the upper-stream fork:

- **premium train:**
  - authelia
  - grafana
  - nextcloud
  - prometheus
  - traefik

- **stable train**
  - anything-llm
  - audiobookshelf
  - autobrr
  - bazarr
  - changedetection.io
  - cloudflared
  - code-server
  - codeproject-ai-server
  - crafty-4
  - factorio
  - frigate
  - flaresolverr
  - gamevault-backend
  - home-assistant
  - immich
  - jellyfin
  - jellystat
  - lidarr
  - lldap
  - local-ai
  - maintainerr
  - meshcentral
  - minio
  - nzbget
  - ollama
  - paperless-ngx
  - plex
  - prowlarr
  - qbitmanage
  - qBittorrent
  - radarr
  - readarr
  - recyclarr
  - satisfactory
  - sabnzbd
  - sftpgo
  - sonarr
  - stun-turn-server
  - syncthing
  - tautulli
  - tdarr
  - unpackerr


### How to update other charts in this catalog:

This fork comes with a semi-automatic updater in `updater` which checks for newer images of apps specified in `updater/config.py` and creates corresponding charts to use the latest images. You can add an app into the configuration, e.g.

```python
import pathlib

CHARTS_DIR = <path/to/this/project>
APPS = [
    {
        "name": "wg-easy",                  # Name of the chart
        "train": "stable",                  # Train
        "check_ver": {
            "type": "ghcr",                 # Where to look for newer images. GitHub (ghcr) or DockerHub (dockerhub)
            "package_owner": "wg-easy",     # <package_owner>/<package_name> is the repo for the images
            "package_name": "wg-easy",
            "anchor_tag": "latest",         # [Optional] Only images with the <anchor_tag> are considered when updating.
            "version_matcher": r"^\d+$",    # [Optional] To extract version from tag
            "version_rewriter": "{}.0.0"    # [Optional] Rewrite the version from tag into another format
        },
    }
    ...
]
```

Then, by running

```bash
cd <path/to/this/project>/updater
python update.py
```

It honestly replicates the follwoing steps used by the upper-stream fork:

1. `catalog.json`:
   Search for your application and update following part for your app
   ```"latest_version": "3.0.9",
            "latest_app_version": "2.0.3",
            "latest_human_version": "2.0.3_3.0.9",
            "last_update": "2024-05-29 12:35:14",
   ```
   - **latest_version**: `3.0.9` --> `3.1.0` (bump the _chart_ version one version up)
   - **latest_app_version**: `2.0.3` --> `3.1.0` (insert the _app_ version you're updating to)
   - **latest_human_version**: `2.0.3_3.0.9` --> `2.1.0_3.1.0` (_chart_ version & _app_ version combined together)
   - **last_update**: `2024-05-29 12:35:14` --> `2024-09-03 17:00:00` (take the approx. date & time when you're updating the app)
2. `stable\maintainerr\app_versions.json`:
   Dublicate everything between
   ```
    "3.0.9": {
        "healthy": true,
        "supported": true,
        "healthy_error": null,
   ```
   and
   ```
    },
   ```
   just before these lines where the information for the next older version starts:
   ```
    "3.0.9": {
        "healthy": true,
        "supported": true,
        "healthy_error": null,
   ```
   - Change these occurances:
     - 1x `2024-05-29 12:35:14` (take the date & time value you used at step one when modifying `catalog.json`)
     - 2x `2.0.3` (take the _app_ version value you used at step one when modifying `catalog.json`)
     - 5x `3.0.9` (take the _chart_ version value you used at step one when modifying `catalog.json`)
3. Dublicate the folder `stable\maintainerr\3.0.9` and change the folder name to the _chart_ version value you used at step one when modifying `catalog.json`
4. Change these occurances within `stable\maintainerr\3.1.0\Chart.yaml`:
   - 1x `2.0.3` (take the _app_ version value you used at step one when modifying `catalog.json`)
   - 1x `3.0.9` (take the _chart_ version value you used at step one when modifying `catalog.json`)
5. `stable\maintainerr\3.1.0\ix_values.yaml`:
   Update these lines where the image is specified:
   ```
   	image:
   	repository: jorenn92/maintainerr
   	pullPolicy: IfNotPresent
   	tag: 2.0.3@sha256:712e990afff98767a880284eb914fd5f2f5d76c5e8838c3f003fecdeb045b912
   ```
   With some exceptions I always use the images which TrueCharts uses. I copy them from the TrueCharts repository:
   https://github.com/truecharts/charts/blob/master/charts/stable/maintainerr/values.yaml
