import pathlib

APPS = [
    {
        "name": "flood",
        "train": "stable",
        "check_ver": {
            "type": "dockerhub",
            "package_owner": "jesec",
            "package_name": "flood",
            "anchor_tag": "latest",
            "version_matcher": r"\d+(\.\d+)+$"
        }
    },
    {
        "name": "navidrome",
        "train": "stable",
        "check_ver": {
            "type": "dockerhub",
            "package_owner": "deluan",
            "package_name": "navidrome",
            "anchor_tag": "latest",
            "version_matcher": r"\d+(\.\d+)+$",
        },
    },
    {
        "name": "komga",
        "train": "stable",
        "check_ver": {
            "type": "dockerhub",
            "package_owner": "gotson",
            "package_name": "komga",
            "anchor_tag": "latest",
            "version_matcher": r"\d+(\.\d+)+$",
        },
    },
    {
        "name": "nginx-proxy-manager",
        "train": "stable",
        "check_ver": {
            "type": "dockerhub",
            "package_owner": "jc21",
            "package_name": "nginx-proxy-manager",
            "anchor_tag": "latest",
            "version_matcher": r"\d+(\.\d+)+$",
        },
    },
    {
        "name": "alist",
        "train": "stable",
        "check_ver": {
            "type": "dockerhub",
            "package_owner": "xhofe",
            "package_name": "alist-aria2",
            "anchor_tag": "latest",
            "version_matcher": r"\d+(\.\d+)+$",
        },
    },
    {
        "name": "wg-easy",
        "train": "stable",
        "check_ver": {
            "type": "ghcr",
            "package_owner": "wg-easy",
            "package_name": "wg-easy",
            "anchor_tag": "latest",
            "version_matcher": r"^\d+$",
            "version_rewriter": "{}.0.0"
        },
    },
    {
        "name": "tachidesk-docker",
        "train": "stable",
        "check_ver": {
            "type": "ghcr",
            "package_owner": "suwayomi",
            "package_name": "tachidesk",
            "anchor_tag": "preview",
            "version_rewriter": "preview"
        },
    },
]

CHARTS_DIR = pathlib.Path(__file__).parent.parent
