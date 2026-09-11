"""
event_flags.py

This is the missing piece alfizari's editor doesn't provide: reading the
per-location "has this world item been picked up" event flag bits.

Prayer Beads all share one stackable item_id, so inventory quantity alone
can't tell you WHICH bead(s) you have. The game instead flips a unique
event flag per pickup location, matching the item lot IDs in your data
dump (e.g. lot 1010, 1020, 1060, 1500, 1140, 1560 = "Prayer Bead" rows).

FLAG_TABLE_OFFSET below is UNKNOWN and must be found empirically -- see
find_flag_table_offset() for a diffing strategy. Once you find it, the
rest of this module (bit indexing/reading) should just work, since FromSoft
event flag tables are a straightforward packed bit array indexed by flag ID.
"""

from __future__ import annotations

# --- TO BE DISCOVERED -------------------------------------------------
# Byte offset (relative to the start of a slot's 1MB blob) where the
# event flag bit array begins.
FLAG_TABLE_OFFSET: int | None = None
# ------------------------------------------------------------------------


def read_flag(slot_data: bytes, flag_id: int, table_offset: int | None = None) -> bool | None:
    """Read a single event flag's boolean state, or None if the flag table
    offset hasn't been discovered yet (run find_flag_table_offset() first).

    FromSoft event flags are typically packed MSB-first within each byte,
    indexed by flag_id. This matches the layout used across the DS/Sekiro
    family -- verify against a couple of known flags before trusting it.
    """
    offset = table_offset if table_offset is not None else FLAG_TABLE_OFFSET
    if offset is None:
        return None
    byte_index = flag_id // 8
    bit_index = 7 - (flag_id % 8)  # MSB-first; flip to `flag_id % 8` if wrong
    byte = slot_data[offset + byte_index]
    return bool((byte >> bit_index) & 1)


def find_flag_table_offset(before: bytes, after: bytes, chunk_size: int = 0x2000) -> list[int]:
    """Diff two same-slot snapshots (before/after picking up ONE known
    item, saved and re-read in between) and return byte offsets where
    exactly one or a few bits differ -- candidate locations for the flag
    table. Run this a few times with different single pickups and
    intersect the candidate offsets to narrow it down fast.
    """
    if len(before) != len(after):
        raise ValueError("snapshots must be the same length (same slot layout)")

    candidates = []
    for offset in range(0, len(before) - chunk_size, chunk_size):
        b_chunk = before[offset:offset + chunk_size]
        a_chunk = after[offset:offset + chunk_size]
        if b_chunk == a_chunk:
            continue
        diff_bytes = sum(1 for x, y in zip(b_chunk, a_chunk) if x != y)
        # A flag flip changes exactly one byte by exactly one bit (a small
        # value change). Inventory/stat changes tend to touch many bytes
        # or larger multi-byte values -- so favor chunks with few diffs.
        if diff_bytes <= 3:
            candidates.append(offset)
    return candidates
