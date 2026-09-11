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
    name: str            # display name for tracker UI
    region: str           # in-game area
    item_lot_id: int | None = None  # from the item lot dump; None until confirmed
    event_flag_id: int | None = None  # fill in once discovered
    notes: str = ""


PRAYER_BEADS: list[BeadLocation] = [


# --------------------------
# Bosses / Mini Bosses 
# --------------------------

BeadLocation("Samurai general Naomori Kawaradi", "Ashina Outskirts" , event_flag_id = 6723, notes="#1"),
BeadLocation("Chained Ogre", "Ashina Outskirts", item_lot_id = None , event_flag_id = 6710, notes="#2"),
BeadLocation("Samurai General Tenzen Yamauchi", "Ashina Outskirts", item_lot_id = None , event_flag_id = 6762, notes="#3"),
BeadLocation("Blazing Bull", "Ashina Outskirts", item_lot_id = None , event_flag_id = 6711, notes="#5"),
BeadLocation("Shinobi Hunter Enshin of Misen", "Hirata Estate", item_lot_id = None , event_flag_id = 6763, notes="#6"),
BeadLocation("Juzuo the Drunkard ", "Hirata Estate", item_lot_id = None , event_flag_id = 6764, notes="#7"),
BeadLocation("Lone Shadow Swordsman - Depths Cave", "Ashina Castle", item_lot_id = None , event_flag_id = 6770, notes="#9"),
BeadLocation("Seven Spears Shikibu Toshikatsu", "Ashina Castle", item_lot_id = None , event_flag_id = 6769, notes="#10"),
BeadLocation("Samurai General Kuramosuke Matsumoto", "Ashina Castle", item_lot_id = None , event_flag_id = None, notes="#11"),
BeadLocation("Ashina Elite Jinsuke Saze", "Ashina Castle", item_lot_id = None , event_flag_id = 6767, notes="#13"),
BeadLocation("Snake Eyes - Gun Fort", "Sunken Valley", item_lot_id = None , event_flag_id = 6773, notes="#16"),
BeadLocation("Long-Armed Centipede Giraffe", "Sunken Valley", item_lot_id = None , event_flag_id = 6774, notes="#17"),
BeadLocation("Armored Warrior", "Senpou Temple", item_lot_id = None , event_flag_id = 6715, notes="#19"),
BeadLocation("Long-Armed Centipede Sen'un", "", item_lot_id = None , event_flag_id = 6772, notes="#20"),
BeadLocation("Snake Eyes Shirafuji", "Ashina Depths", item_lot_id = None , event_flag_id = 6775, notes="#23"),
BeadLocation("Dual Ape - Bead Drop 1", "Ashina Depths", item_lot_id = None , event_flag_id = None, notes="#24"),
BeadLocation("Dual Ape - Bead Drop 2", "Ashina Depths", item_lot_id = None , event_flag_id = None, notes="#25"),
BeadLocation("Tojujiro the Glutton - Hidden Forest", "Ashina Depths", item_lot_id = None , event_flag_id = None, notes="#26"),
BeadLocation("O'rin of the Water", "Ashina Depths", item_lot_id = None , event_flag_id = None, notes="#27"),
BeadLocation("Chained Ogre Antechamber", "Ashina Castle (Dusk)", item_lot_id = None , event_flag_id = None, notes="#30"),
BeadLocation("Lone Shadow Masanaga the Spear Bearer", "Ashina Castle (Dusk)", item_lot_id = None , event_flag_id = None, notes="#31"),
BeadLocation("Lone Shadow Vilehand - Upper Dojo", "Ashina Castle (Dusk)", item_lot_id = None , event_flag_id = None, notes="#32"),
BeadLocation("Lone Shadow Masanaga - Past", "Hirata Estate (Owls Memory)", item_lot_id = None , event_flag_id = None, notes="#33"),
BeadLocation("Juzou the Drunkard - Past", "Hirata Estate (Owls Memory)", item_lot_id = None , event_flag_id = None, notes="#34"),
BeadLocation("Sakura Bull of the Palace", "Fountainhead Palace", item_lot_id = None , event_flag_id = None, notes="#35"),
BeadLocation("Okami Leader Shizu", "Fountainhead Palace", item_lot_id = None , event_flag_id = None, notes="#36"),
BeadLocation("Red-Eyes Ashina Elite", "Ashina Castle (Night)", item_lot_id = None , event_flag_id = None, notes="#38"),
BeadLocation("Shigekichi of the Red Guard - Drunkard", "Ashina Castle  (Night)", item_lot_id = None , event_flag_id = None, notes="#39"),
BeadLocation("Seven Ashina Spears - Ashina Reservoir", "Ashina Castle (Night)", item_lot_id = None , event_flag_id = None, notes="#40"),
    
#--------------------------
# Treasure / Floor Pickups
#--------------------------

BeadLocation("Attic Chest, Ashina Castle Gate", "Ashina Outskirts", item_lot_id = None , event_flag_id = 6788, notes="#4"),
BeadLocation("Hidden Wall - Main Hall", "Hirata Estate", item_lot_id = None , event_flag_id = 6789, notes="#8"),
BeadLocation("Hidden Wall - Map Room", "Ashina Castle", item_lot_id = None , event_flag_id = 6790, notes="#12"),
BeadLocation("Grave Mounds", "Sunken Valley", item_lot_id = None , event_flag_id = 6792, notes="#15"),
BeadLocation("Floor Boards - Cave System", "Sunken Valley", item_lot_id = None , event_flag_id = 6793, notes="#18"),
BeadLocation("Pond Cave - Buddha Statue", "Senpou Temple", item_lot_id = None , event_flag_id = None, notes="#22"),
BeadLocation("Poison Lake - Buddha Head", "Ashina Depths", item_lot_id = None , event_flag_id = 6794, notes="#24"),
BeadLocation("Head Priests Temple - Hidden Attic Shrine", "Ashina Depths", item_lot_id = None , event_flag_id = None, notes="#28"),
BeadLocation("Mibu Village River Chest", "Ashina Depths", item_lot_id = None , event_flag_id = None, notes="#29"),
BeadLocation("Underwater Chest - Carp Sceleton", "Fountainhead Palace", item_lot_id = None , event_flag_id = None, notes="#37"),

#--------------------------
# Shop Purchases
#--------------------------

BeadLocation("Dungeon Entrance Merchent", "Ashina Castle", event_flag_id = 6768, notes="#14")

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
    return result
