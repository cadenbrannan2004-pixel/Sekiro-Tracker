"""
event_flags.py

"""

from __future__ import annotations

BLOCK_OFFSETS: dict[int, int] = {
    6: 0x334,
}


def read_flag(slot_data: bytes, flag_id: int) -> bool | None:
    """True/False for a flag, or None if its block's offset isn't known yet."""
    block_start = BLOCK_OFFSETS.get(flag_id // 1000)
    if block_start is None:
        return None
    m = flag_id % 1000
    word_offset = block_start + (m // 32) * 4
    word = int.from_bytes(slot_data[word_offset:word_offset + 4], "little")
    return bool(word & (1 << (31 - m % 32)))