"""
steam_achievements.py

Reads the account's Sekiro achievements from Steam's local stats cache, so
progress counts every playthrough instead of only the current save.

"""

from __future__ import annotations

import struct
from pathlib import Path

APP_ID = 814380
STEAM_ID64_BASE = 76561197960265728  # steamid64 - this = the account id in file names
DEFAULT_STEAM_PATH = Path("C:/Program Files (x86)/Steam")


def _steam_registry(subkey: str, value: str):
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, rf"Software\Valve\Steam{subkey}") as key:
            return winreg.QueryValueEx(key, value)[0]
    except (ImportError, OSError):
        return None


def steam_path() -> Path:
    path = _steam_registry("", "SteamPath")
    return Path(path) if path else DEFAULT_STEAM_PATH


def active_steam_id64() -> int | None:
    """steamid64 of whoever is signed in to Steam on this PC, or None if nobody is."""
    account_id = _steam_registry(r"\ActiveProcess", "ActiveUser")
    return STEAM_ID64_BASE + account_id if account_id else None


def _parse_kv(data: bytes, i: int = 0) -> tuple[dict, int]:
    """Binary KeyValues: type byte, null-terminated key, value; 0x08 ends a block."""
    out = {}
    while True:
        kind = data[i]
        i += 1
        if kind == 0x08:
            return out, i
        end = data.index(0, i)
        key = data[i:end].decode("utf-8", "replace")
        i = end + 1
        if kind == 0x00:
            value, i = _parse_kv(data, i)
        elif kind == 0x01:
            end = data.index(0, i)
            value = data[i:end].decode("utf-8", "replace")
            i = end + 1
        elif kind == 0x02:
            value = struct.unpack_from("<i", data, i)[0]
            i += 4
        elif kind == 0x03:
            value = struct.unpack_from("<f", data, i)[0]
            i += 4
        elif kind == 0x07:
            value = struct.unpack_from("<Q", data, i)[0]
            i += 8
        else:
            raise ValueError(f"unknown KeyValues type 0x{kind:02X} at byte {i - 1}")
        out[key] = value


def _read_kv(path: Path) -> dict:
    with open(path, "rb") as f:
        return _parse_kv(f.read())[0]


def read_achievements(steam_id64: int) -> dict[str, bool] | None:
    """English achievement name -> unlocked, or None if Steam's cache isn't there."""
    stats_dir = steam_path() / "appcache" / "stats"
    schema_path = stats_dir / f"UserGameStatsSchema_{APP_ID}.bin"
    user_path = stats_dir / f"UserGameStats_{steam_id64 - STEAM_ID64_BASE}_{APP_ID}.bin"
    try:
        schema = _read_kv(schema_path)[str(APP_ID)]["stats"]
        user = _read_kv(user_path).get("cache", {})
    except (OSError, KeyError, ValueError, IndexError, struct.error):
        return None

    result = {}
    for stat_id, stat in schema.items():
        # A stat with nothing unlocked yet may be missing from the user file
        bits = user.get(stat_id, {}).get("data", 0)
        for bit, ach in stat.get("bits", {}).items():
            name = ach.get("display", {}).get("name", {})
            if isinstance(name, dict):
                name = name.get("english", ach.get("name", ""))
            result[name] = bool(bits & (1 << int(bit)))
    return result
