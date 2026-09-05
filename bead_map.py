"""
bead_map.py

Prayer Bead pickup locations, seeded from the item lot dump you already
have. `item_lot_id` is confirmed from that data; `event_flag_id` is what
you still need to fill in per-location (see event_flags.find_flag_table_offset
and cross-reference against SoulSplitter's Sekiro event flag list / a
Sekiro fan wiki's item location pages, which document flag IDs per pickup).

Note: some lot IDs in the dump (e.g. 1010/1020 "Prayer Bead") were tagged
[Unused/Unknown] with no location -- only include entries here once you've
confirmed they're real, reachable world pickups, not cut content.
"""

from dataclasses import dataclass


@dataclass
class BeadLocation:
    name: str            # display name for your tracker UI
    region: str           # in-game area
    item_lot_id: int      # from the item lot dump
    event_flag_id: int | None = None  # fill in once discovered
    notes: str = ""


# Seed list -- expand/verify against the full dump and in-game locations.
# This is intentionally incomplete; treat it as a starting skeleton.
PRAYER_BEADS: list[BeadLocation] = [


# --------------------------
# Bosses / Mini Bosses 
# --------------------------

BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),

#--------------------------
# Treasure / Floor Pickups
#--------------------------

BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),
BeadLocation("", "", item_lot_id = None , event_flag_id = None, notes=""),

#--------------------------
# Shop Purchases
#--------------------------

BeadLocation("", "", event_flag_id = None, notes=""),



]

"""Return {bead_name: picked_up_bool} for every mapped bead."""

def get_bead_state(slot_data: bytes) -> dict[str, bool]:

    # local import to avoid unused-arg lint noise
    from event_flags import read_flag  

    result = {}
    for bead in PRAYER_BEADS:
        if bead.event_flag_id is None:
            result[bead.name] = None  # not yet mapped
            continue
        result[bead.name] = read_flag(slot_data, bead.event_flag_id)
    return results
