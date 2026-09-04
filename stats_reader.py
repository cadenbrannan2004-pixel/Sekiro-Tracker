"""
stats_reader.py

Minimal scalar stat reads, ported from alfizari's confirmed offsets.
Not needed for achievement tracking itself -- this exists purely so you
have something immediately recognizable to eyeball-check against your
real character, to confirm the save file / slot you're reading is
actually the one you think it is.
"""

import struct

STEAM_ID_OFFSET = 0x33E54
ATTACK_OFFSET = 0x3449C
NG_PLUS_OFFSET = 0x33F34
GUARD_OFFSET = 0x34488
EMBLEM_OFFSET = 0x3459A
SKILL_POINTS_OFFSET = 0x345B4
HP_OFFSET = 0x3446C
SOULS_OFFSET = 0x344D0


def read_stats(slot_data: bytes) -> dict:
    """Returns basic stats for a quick human sanity-check. Wrapped in
    try/except per-field since an empty/unused slot may not have valid
    data at these offsets."""
    stats = {}
    try:
        stats["steam_id"] = struct.unpack_from("<Q", slot_data, STEAM_ID_OFFSET)[0]
        stats["attack"] = struct.unpack_from("<B", slot_data, ATTACK_OFFSET)[0]
        stats["ng_plus"] = struct.unpack_from("<B", slot_data, NG_PLUS_OFFSET)[0]
        stats["guard"] = struct.unpack_from("<I", slot_data, GUARD_OFFSET)[0]
        stats["emblems"] = struct.unpack_from("<B", slot_data, EMBLEM_OFFSET)[0]
        stats["skill_points"] = struct.unpack_from("<I", slot_data, SKILL_POINTS_OFFSET)[0]
        stats["hp"] = struct.unpack_from("<I", slot_data, HP_OFFSET)[0]
        stats["sen"] = struct.unpack_from("<I", slot_data, SOULS_OFFSET)[0]
    except struct.error:
        pass
    return stats
