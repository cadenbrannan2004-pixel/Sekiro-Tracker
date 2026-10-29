
from __future__ import annotations

# Byte offset within the slot data where each flag block starts, keyed by
# block number (flag_id // 1000). Offsets are found empirically with
# find_offset.py / scan_offset.py; blocks not listed here are unknown.
BLOCK_OFFSETS: dict[int, int] = {
    6: 0x334,  # flags 6000-6999 (includes the prayer bead flags)
}


def read_flag(slot_data: bytes, flag_id: int) -> bool | None:
    """True/False for a flag, or None if its block's offset isn't known yet."""
    block_start = BLOCK_OFFSETS.get(flag_id // 1000)
    if block_start is None:
        return None

    # Position of the flag inside its block.
    m = flag_id % 1000

    # Each word holds 32 flags and is 4 bytes wide.
    word_offset = block_start + (m // 32) * 4
    word = int.from_bytes(slot_data[word_offset:word_offset + 4], "little")

    # Flags fill each word from the most significant bit down: the first flag
    # in a word is bit 31 (0x80000000), the 32nd is bit 0 (0x00000001).
    return bool(word & (1 << (31 - m % 32)))


def flag_state(locations, slot_data: bytes) -> list[dict]:
    """One row per location, in list order; collected is None if its flag isn't mapped yet."""
    return [
        {
            "name": loc.name,
            "region": loc.region,
            "source": loc.source,
            "video": loc.video,
            "collected": None if loc.event_flag_id is None else read_flag(slot_data, loc.event_flag_id),
        }
        for loc in locations
    ]
