"""
save_reader.py

Handles locating and loading the Sekiro PC save file, and extracting a
single character slot's raw bytes. Slot layout (BND container) confirmed
from alfizari/Sekiro-Save-Editor:

    [0x000, 0x300)   header
    10x slots, each:
        [start, start + 0x100000)  userdata (the 1MB blob we care about)
        + 0x10 bytes of inter-slot padding/checksum
    remainder                      footer

All the "offset" constants elsewhere in this project (inventory, keys,
stats, and eventually event flags) are relative to the START of one
slot's 1MB blob, not the whole file.
"""

import os
import struct
from pathlib import Path

SLOT_SIZE = 0x100000
SLOT_STRIDE = 0x100010  # slot size + inter-slot padding
HEADER_SIZE = 0x300
FIRST_SLOT_OFFSET = 0x310
NUM_SLOTS = 10


def default_save_path() -> Path | None:
    """Best-effort guess at the PC save location. Returns the first
    S0000.sl2 found under the standard Sekiro save directory, or None."""
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return None
    root = Path(appdata) / "Sekiro"
    if not root.exists():
        return None
    for steam_id_dir in root.iterdir():
        candidate = steam_id_dir / "S0000.sl2"
        if candidate.exists():
            return candidate
    return None


def read_save_file(path: Path) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def extract_slot(full_save_data: bytes, slot_index: int) -> bytes:
    """Return the raw 1MB blob for a given character slot (0-9)."""
    if not (0 <= slot_index < NUM_SLOTS):
        raise ValueError(f"slot_index must be 0-{NUM_SLOTS - 1}")
    start = FIRST_SLOT_OFFSET + slot_index * SLOT_STRIDE
    return full_save_data[start:start + SLOT_SIZE]


def find_active_slots(full_save_data: bytes) -> list[int]:
    """Return indices of slots that look non-empty (very rough heuristic:
    not all zero in the first chunk of the slot). Refine this once you
    know a better 'slot in use' marker."""
    active = []
    for i in range(NUM_SLOTS):
        slot = extract_slot(full_save_data, i)
        if any(b != 0 for b in slot[:0x1000]):
            active.append(i)
    return active
