
import os
import struct
from pathlib import Path

from steam_achievements import active_steam_id64

SLOT_SIZE = 0x100000
SLOT_STRIDE = 0x100010  # slot size + inter-slot padding
HEADER_SIZE = 0x300
FIRST_SLOT_OFFSET = 0x310
NUM_SLOTS = 10
# One byte per slot (1 = in use) in the summary block after the slots. Deleting
# a character only clears this flag; the slot's data is left behind.
# Found with `find_offset.py tail`.
ACTIVE_FLAGS_OFFSET = 0xA00484


def default_save_path() -> Path | None:
    """Best-effort guess at the PC save location. Each Steam account gets its
    own %APPDATA%\\Sekiro\\<steamid64> folder, so this prefers the account
    signed in to Steam, then the most recently saved S0000.sl2, or None."""
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return None
    root = Path(appdata) / "Sekiro"
    if not root.exists():
        return None

    active = active_steam_id64()
    if active is not None:
        candidate = root / str(active) / "S0000.sl2"
        if candidate.exists():
            return candidate

    saves = [d / "S0000.sl2" for d in root.iterdir() if (d / "S0000.sl2").exists()]
    return max(saves, key=lambda p: p.stat().st_mtime, default=None)


def save_owner_steam_id64(save_path: Path) -> int | None:
    """The steamid64 a save belongs to, from its folder name."""
    name = save_path.parent.name
    return int(name) if name.isdigit() else None


def read_save_file(path: Path) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def extract_slot(full_save_data: bytes, slot_index: int) -> bytes:
    """Return the raw 1MB blob for a given character slot (0-9)."""
    if not (0 <= slot_index < NUM_SLOTS):
        raise ValueError(f"slot_index must be 0-{NUM_SLOTS - 1}")
    start = FIRST_SLOT_OFFSET + slot_index * SLOT_STRIDE
    return full_save_data[start : start + SLOT_SIZE]


def find_active_slots(full_save_data: bytes) -> list[int]:
    """Return indices of slots the game marks as in use."""
    flags = full_save_data[ACTIVE_FLAGS_OFFSET : ACTIVE_FLAGS_OFFSET + NUM_SLOTS]
    if len(flags) == NUM_SLOTS:
        return [i for i, flag in enumerate(flags) if flag == 1]

    # File too short to hold the flags: fall back to "slot isn't all zero"
    active = []
    for i in range(NUM_SLOTS):
        slot = extract_slot(full_save_data, i)
        if any(slot[:0x1000]):
            active.append(i)
    return active
