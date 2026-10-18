"""
bead_map.py

Prayer Bead pickup locations

"""

from dataclasses import dataclass

from event_flags import flag_state


@dataclass
class BeadLocation:
    name: str            # display name for tracker UI
    region: str           # in-game area
    event_flag_id: int | None = None  # filled in once discovered empirically and needed for tracker
    notes: str = ""


PRAYER_BEADS: list[BeadLocation] = [


# --------------------------
# Bosses / Mini Bosses 
# --------------------------

BeadLocation("Samurai general Naomori Kawaradi", "Ashina Outskirts" , event_flag_id = 6723, notes="#1"),
BeadLocation("Chained Ogre", "Ashina Outskirts", event_flag_id = 6710, notes="#2"),
BeadLocation("Samurai General Tenzen Yamauchi", "Ashina Outskirts", event_flag_id = 6762, notes="#3"),
BeadLocation("Blazing Bull", "Ashina Outskirts", event_flag_id = 6711, notes="#5"),
BeadLocation("Shinobi Hunter Enshin of Misen", "Hirata Estate", event_flag_id = 6763, notes="#6"),
BeadLocation("Juzuo the Drunkard ", "Hirata Estate", event_flag_id = 6764, notes="#7"),
BeadLocation("Lone Shadow Swordsman - Depths Cave", "Ashina Castle", event_flag_id = 6770, notes="#9"),
BeadLocation("Seven Spears Shikibu Toshikatsu", "Ashina Castle", event_flag_id = 6769, notes="#10"),
BeadLocation("Samurai General Kuramosuke Matsumoto", "Ashina Castle", event_flag_id = None, notes="#11"),
BeadLocation("Ashina Elite Jinsuke Saze", "Ashina Castle", event_flag_id = 6767, notes="#13"),
BeadLocation("Snake Eyes - Gun Fort", "Sunken Valley", event_flag_id = 6773, notes="#16"),
BeadLocation("Long-Armed Centipede Giraffe", "Sunken Valley", event_flag_id = 6774, notes="#17"),
BeadLocation("Armored Warrior", "Senpou Temple", event_flag_id = 6715, notes="#19"),
BeadLocation("Long-Armed Centipede Sen'un", "Senpou Temple", event_flag_id = 6772, notes="#20"),
BeadLocation("Snake Eyes Shirafuji", "Ashina Depths", event_flag_id = 6775, notes="#23"),
BeadLocation("Dual Ape - Bead Drop 1", "Ashina Depths", event_flag_id = 6798, notes="#24"),
BeadLocation("Dual Ape - Bead Drop 2", "Ashina Depths", event_flag_id = 6799, notes="#25"),
BeadLocation("Tojujiro the Glutton - Hidden Forest", "Ashina Depths", event_flag_id = 6776, notes="#26"),
BeadLocation("O'rin of the Water", "Ashina Depths", event_flag_id = None, notes="#27"),
BeadLocation("Chained Ogre Antechamber", "Ashina Castle (Dusk)", event_flag_id = 6778, notes="#30"),
BeadLocation("Lone Shadow Masanaga the Spear Bearer", "Ashina Castle (Dusk)", event_flag_id = 6780, notes="#31"),
BeadLocation("Lone Shadow Vilehand - Upper Dojo", "Ashina Castle (Dusk)", event_flag_id = 6779, notes="#32"),
BeadLocation("Lone Shadow Masanaga - Past", "Hirata Estate (Owls Memory)", event_flag_id = 6781, notes="#33"),
BeadLocation("Juzou the Drunkard - Past", "Hirata Estate (Owls Memory)", event_flag_id = 6782, notes="#34"),
BeadLocation("Sakura Bull of the Palace", "Fountainhead Palace", event_flag_id = 6783, notes="#35"),
BeadLocation("Okami Leader Shizu", "Fountainhead Palace", event_flag_id = 6784, notes="#36"),
BeadLocation("Red-Eyes Ashina Elite", "Ashina Castle (Night)", event_flag_id = 6785, notes="#38"),
BeadLocation("Shigekichi of the Red Guard - Drunkard", "Ashina Castle  (Night)", event_flag_id = 6787, notes="#39"),
BeadLocation("Seven Ashina Spears - Ashina Reservoir", "Ashina Castle (Night)", event_flag_id = 6786, notes="#40"),
    
#--------------------------
# Treasure / Floor Pickups
#--------------------------

BeadLocation("Attic Chest, Ashina Castle Gate", "Ashina Outskirts", event_flag_id = 6788, notes="#4"),
BeadLocation("Hidden Wall - Main Hall", "Hirata Estate", event_flag_id = 6789, notes="#8"),
BeadLocation("Hidden Wall - Map Room", "Ashina Castle", event_flag_id = 6790, notes="#12"),
BeadLocation("Grave Mounds", "Sunken Valley", event_flag_id = 6792, notes="#15"),
BeadLocation("Floor Boards - Cave System", "Sunken Valley", event_flag_id = 6793, notes="#18"),
BeadLocation("Pond Cave - Buddha Statue", "Senpou Temple", event_flag_id = 6791, notes="#22"),
BeadLocation("Poison Lake - Buddha Head", "Ashina Depths", event_flag_id = 6794, notes="#21"),
BeadLocation("Head Priests Temple - Hidden Attic Shrine", "Ashina Depths", event_flag_id = 6795, notes="#28"),
BeadLocation("Mibu Village River Chest", "Ashina Depths", event_flag_id = 6796, notes="#29"),
BeadLocation("Underwater Chest - Carp Skeleton", "Fountainhead Palace", event_flag_id = 6797, notes="#37"),

#--------------------------
# Shop Purchases
#--------------------------

BeadLocation("Dungeon Entrance Merchent", "Ashina Castle", event_flag_id = 6768, notes="#14")

]


def get_bead_state(slot_data: bytes) -> dict[str, bool | None]:
    return flag_state(PRAYER_BEADS, slot_data)
