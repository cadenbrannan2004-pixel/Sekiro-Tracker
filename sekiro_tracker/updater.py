import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

VERSION = "1.1.0"
LATEST_RELEASE = (
    "https://api.github.com/repos/cadenbrannan2004-pixel/Sekiro-Tracker/releases/latest"
)
ASSET_NAME = "SekiroTracker.exe"
FROZEN = getattr(sys, "frozen", False)  # only the built exe can replace itself


def _parse(tag: str) -> tuple[int, ...]:
    return tuple(int(part) for part in tag.lstrip("v").split("."))


def check() -> dict | None:
    """The latest release if it's newer than this build, otherwise None. Never raises."""
    if not FROZEN:
        return None
    try:
        with urllib.request.urlopen(LATEST_RELEASE, timeout=5) as res:
            release = json.load(res)
        if _parse(release["tag_name"]) <= _parse(VERSION):
            return None
        asset = next(a for a in release["assets"] if a["name"] == ASSET_NAME)
        return {
            "version": release["tag_name"],
            "url": asset["browser_download_url"],
            # No checksum published = no update, rather than running an unverified file
            "sha256": asset["digest"].removeprefix("sha256:"),
        }
    except (
        Exception
    ):  # offline, rate-limited, odd tag like v2.0-beta: just skip this launch
        return None


def install(update: dict) -> None:
    """Downloads and verifies the new exe, swaps it in and starts it. The caller then exits."""
    exe = Path(sys.executable)
    new = exe.with_name(exe.name + ".new")
    old = exe.with_name(exe.name + ".old")

    sha = hashlib.sha256()
    with urllib.request.urlopen(update["url"], timeout=60) as res, open(new, "wb") as f:
        while chunk := res.read(1 << 16):
            sha.update(chunk)
            f.write(chunk)
    if sha.hexdigest() != update["sha256"]:
        new.unlink()
        raise ValueError(
            "The download didn't match GitHub's checksum, so it was discarded"
        )

    # Windows won't overwrite a running exe but will rename it
    old.unlink(missing_ok=True)
    exe.rename(old)
    try:
        new.rename(exe)
    except OSError:
        old.rename(exe)  # put the working exe back
        raise

    # Without this the new onefile exe reuses this process's temp folder, which is deleted when we exit
    subprocess.Popen(
        [str(exe)], env={**os.environ, "PYINSTALLER_RESET_ENVIRONMENT": "1"}
    )


def remove_leftover() -> None:
    """Deletes the previous exe after an update. It may still be closing, so retry next launch."""
    try:
        Path(sys.executable + ".old").unlink(missing_ok=True)
    except OSError:
        pass
