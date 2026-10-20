"""
bead_map.py

Prayer Bead pickup locations

"""

from dataclasses import dataclass

from event_flags import flag_state


# How the item is obtained, shown next to it in the UI
BOSS = "Boss drop"
CHEST = "Chest"
PICKUP = "Pickup"
SHOP = "Shop"


@dataclass
class BeadLocation:
    name: str  # display name for tracker UI
    region: str  # in-game area
    source: str  # BOSS / CHEST / PICKUP / SHOP
    event_flag_id: int | None = (
        None  # filled in once discovered empirically and needed for tracker
    )
    notes: str = ""
    video: str = ""  # YouTube links


# fmt: off
PRAYER_BEADS: list[BeadLocation] = [
    # --------------------------
    # Pickups / Chests
    # --------------------------
    BeadLocation("Attic Chest, Ashina Castle Gate", "Ashina Outskirts", CHEST, 6788, notes="#4", video=""),
    BeadLocation("Hidden Wall - Main Hall", "Hirata Estate", PICKUP, 6789, notes="#8", video=""),
    BeadLocation("Hidden Wall - Map Room", "Ashina Castle", PICKUP, 6790, notes="#12", video=""),
    BeadLocation("Grave Mounds", "Sunken Valley", PICKUP, 6792, notes="#15", video=""),
    BeadLocation("Floor Boards - Cave System", "Sunken Valley", PICKUP, 6793, notes="#18", video=""),
    BeadLocation("Poison Lake - Buddha Head", "Ashina Depths", PICKUP, 6794, notes="#21", video=""),
    BeadLocation("Pond Cave - Buddha Statue", "Senpou Temple", PICKUP, 6791, notes="#22", video=""),
    BeadLocation("Head Priests Temple - Hidden Attic Shrine", "Ashina Depths", PICKUP, 6795, notes="#28", video=""),
    BeadLocation("Mibu Village River Chest", "Ashina Depths", CHEST, 6796, notes="#29", video=""),
    BeadLocation("Underwater Chest - Carp Skeleton", "Fountainhead Palace", CHEST, 6797, notes="#37", video=""),

    # --------------------------
    # Boss Drops
    # --------------------------
    BeadLocation("Samurai general Naomori Kawaradi", "Ashina Outskirts", BOSS, 6723, notes="#1", video=""),
    BeadLocation("Chained Ogre", "Ashina Outskirts", BOSS, 6710, notes="#2", video=""),
    BeadLocation("Samurai General Tenzen Yamauchi", "Ashina Outskirts", BOSS, 6762, notes="#3", video=""),
    BeadLocation("Blazing Bull", "Ashina Outskirts", BOSS, 6711, notes="#5", video=""),
    BeadLocation("Shinobi Hunter Enshin of Misen", "Hirata Estate", BOSS, 6763, notes="#6", video=""),
    BeadLocation("Juzuo the Drunkard ", "Hirata Estate", BOSS, 6764, notes="#7", video=""),
    BeadLocation("Lone Shadow Swordsman - Depths Cave", "Ashina Castle", BOSS, 6770, notes="#9", video=""),
    BeadLocation("Seven Spears Shikibu Toshikatsu", "Ashina Castle", BOSS, 6769, notes="#10", video=""),
    BeadLocation("Samurai General Kuramosuke Matsumoto", "Ashina Castle", BOSS, notes="#11", video=""),
    BeadLocation("Ashina Elite Jinsuke Saze", "Ashina Castle", BOSS, 6767, notes="#13", video=""),
    BeadLocation("Snake Eyes - Gun Fort", "Sunken Valley", BOSS, 6773, notes="#16", video=""),
    BeadLocation("Long-Armed Centipede Giraffe", "Sunken Valley", BOSS, 6774, notes="#17", video=""),
    BeadLocation("Armored Warrior", "Senpou Temple", BOSS, 6715, notes="#19", video=""),
    BeadLocation("Long-Armed Centipede Sen'un", "Senpou Temple", BOSS, 6772, notes="#20", video=""),
    BeadLocation("Snake Eyes Shirafuji", "Ashina Depths", BOSS, 6775, notes="#23", video=""),
    BeadLocation("Dual Ape - Bead Drop 1", "Ashina Depths", BOSS, 6798, notes="#24", video=""),
    BeadLocation("Dual Ape - Bead Drop 2", "Ashina Depths", BOSS, 6799, notes="#25", video=""),
    BeadLocation("Tojujiro the Glutton - Hidden Forest", "Ashina Depths", BOSS, 6776, notes="#26", video=""),
    BeadLocation("O'rin of the Water", "Ashina Depths", BOSS, notes="#27", video=""),
    BeadLocation("Chained Ogre Antechamber", "Ashina Castle (Dusk)", BOSS, 6778, notes="#30", video=""),
    BeadLocation("Lone Shadow Masanaga the Spear Bearer", "Ashina Castle (Dusk)", BOSS, 6780, notes="#31", video=""),
    BeadLocation("Lone Shadow Vilehand - Upper Dojo", "Ashina Castle (Dusk)", BOSS, 6779, notes="#32", video=""),
    BeadLocation("Lone Shadow Masanaga - Past", "Hirata Estate (Owls Memory)", BOSS, 6781, notes="#33", video=""),
    BeadLocation("Juzou the Drunkard - Past", "Hirata Estate (Owls Memory)", BOSS, 6782, notes="#34", video=""),
    BeadLocation("Sakura Bull of the Palace", "Fountainhead Palace", BOSS, 6783, notes="#35", video=""),
    BeadLocation("Okami Leader Shizu", "Fountainhead Palace", BOSS, 6784, notes="#36", video=""),
    BeadLocation("Red-Eyes Ashina Elite", "Ashina Castle (Night)", BOSS, 6785, notes="#38", video=""),
    BeadLocation("Shigekichi of the Red Guard - Drunkard", "Ashina Castle  (Night)", BOSS, 6787, notes="#39", video=""),
    BeadLocation("Seven Ashina Spears - Ashina Reservoir", "Ashina Castle (Night)", BOSS, 6786, notes="#40", video=""),

    # --------------------------
    # Vendors
    # --------------------------
    BeadLocation("Dungeon Entrance Merchent", "Ashina Castle", SHOP, 6768, notes="#14", video=""),
]
# fmt: on


def get_bead_state(slot_data: bytes) -> list[dict]:
    return flag_state(PRAYER_BEADS, slot_data)
