"""
app_settings.py

Dashboard preferences kept in settings.json. server.py serves and saves them;
tracker.py reads the save file location and refresh rate from here too.
"""

import html
import json
import os
import re
from pathlib import Path

from save_reader import default_save_path

SETTINGS_PATH = Path(__file__).parent / "settings.json"

# Allowed values per setting; anything else sent from the page is ignored
CHOICES = {
    "theme": ("light", "dark"),
    "petals": ("on", "off"),
    "banner": ("on", "off"),
    "hideCollected": ("on", "off"),
    "newHighlight": ("seen", "1m", "5m", "off"),
    "refresh": ("1", "3", "5", "10"),
    "autoClose": ("on", "off"),
    "videos": ("inline", "youtube"),
}
SECTIONS = ("bosses", "beads", "gourds", "tools", "materials", "endings")
DEFAULT_REFRESH_SECONDS = 3


def load() -> dict:
    # tracker.py reads this from another thread, so a missing or half-written file just means defaults
    try:
        with open(SETTINGS_PATH) as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _save(settings: dict) -> None:
    tmp = SETTINGS_PATH.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(settings, f, indent=2)
    os.replace(tmp, SETTINGS_PATH)


def reset() -> None:
    SETTINGS_PATH.unlink(missing_ok=True)


def update(payload: dict) -> str | None:
    """Merges the valid keys of payload into settings.json. Returns an error message, or None."""
    settings = load()

    if "savePath" in payload:
        path = payload["savePath"]
        if not isinstance(path, str):
            return "expected savePath to be a string"
        path = path.strip().strip('"')  # Explorer's "Copy as path" wraps it in quotes
        if path and not Path(path).is_file():
            return f"No file found at {path}"
        if path:
            settings["savePath"] = path
        else:
            settings.pop("savePath", None)  # blank = find it automatically again

    for key, allowed in CHOICES.items():
        if payload.get(key) in allowed:
            settings[key] = payload[key]
    if isinstance(payload.get("selectedSlot"), str):
        settings["selectedSlot"] = payload["selectedSlot"][:8]
    if isinstance(payload.get("hiddenSections"), list):
        settings["hiddenSections"] = [s for s in SECTIONS if s in payload["hiddenSections"]]

    _save(settings)
    return None


def html_attrs(settings: dict) -> str:
    """data-* attributes for the page's <html> tag, e.g. hideCollected -> data-hide-collected="on"."""
    values = {key: settings[key] for key, allowed in CHOICES.items() if settings.get(key) in allowed}
    if isinstance(settings.get("hiddenSections"), list):
        values["hiddenSections"] = " ".join(s for s in SECTIONS if s in settings["hiddenSections"])
    if isinstance(settings.get("selectedSlot"), str):
        values["selectedSlot"] = settings["selectedSlot"]

    attrs = ""
    for key, value in values.items():
        name = re.sub(r"[A-Z]", lambda m: "-" + m.group().lower(), key)
        attrs += f' data-{name}="{html.escape(value)}"'
    return attrs


def save_path() -> Path | None:
    """The save the user picked in Settings, otherwise the auto-detected one."""
    custom = load().get("savePath")
    return Path(custom) if isinstance(custom, str) and custom else default_save_path()


def refresh_seconds() -> int:
    value = load().get("refresh")
    return int(value) if value in CHOICES["refresh"] else DEFAULT_REFRESH_SECONDS
