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
    BeadLocation("Attic Chest, Ashina Castle Gate", "Ashina Outskirts", CHEST, 6788, notes="#4", video="https://youtu.be/TfuiIJTFjg8?si=WV9M4S24Z1lc7P8u&t=72"),
    BeadLocation("Hidden Wall - Main Hall", "Hirata Estate", PICKUP, 6789, notes="#8", video="https://youtu.be/TfuiIJTFjg8?si=o3IlKC-PNLow5TPa&t=118"),
    BeadLocation("Hidden Wall - Map Room", "Ashina Castle", PICKUP, 6790, notes="#12", video="https://youtu.be/TfuiIJTFjg8?si=xSerpeGbx3OsV1yG&t=183"),
    BeadLocation("Grave Mounds", "Sunken Valley", PICKUP, 6792, notes="#15", video="https://youtu.be/TfuiIJTFjg8?si=J7pqghS1_0CyL0ys&t=237"),
    BeadLocation("Floor Boards - Cave System", "Sunken Valley", PICKUP, 6793, notes="#18", video="https://youtu.be/TfuiIJTFjg8?si=U1ic1CHIwVOsB-9c&t=287"),
    BeadLocation("Poison Lake - Buddha Head", "Ashina Depths", PICKUP, 6794, notes="#21", video="https://youtu.be/TfuiIJTFjg8?si=RwuXxISiSJMxDj4u&t=326"),
    BeadLocation("Pond Cave - Buddha Statue", "Senpou Temple", PICKUP, 6791, notes="#22", video="https://youtu.be/TfuiIJTFjg8?si=jajI_nwhUNGm6POE&t=451"),
    BeadLocation("Head Priests Temple - Hidden Attic Shrine", "Ashina Depths", PICKUP, 6795, notes="#28", video="https://youtu.be/TfuiIJTFjg8?si=vOnbzBHAQVaDtTBA&t=399"),
    BeadLocation("Mibu Village River Chest", "Ashina Depths", CHEST, 6796, notes="#29", video="https://youtu.be/TfuiIJTFjg8?si=Q1H42swRfKpvR6w7&t=424"),
    BeadLocation("Underwater Chest - Carp Skeleton", "Fountainhead Palace", CHEST, 6797, notes="#37", video="https://youtu.be/TfuiIJTFjg8?si=ICRatf5X05SaEluN&t=584"),

    # --------------------------
    # Boss Drops
    # --------------------------
    BeadLocation("Samurai general Naomori Kawaradi", "Ashina Outskirts", BOSS, 6723, notes="#1", video="https://youtu.be/TfuiIJTFjg8?si=_LSw6CT0rkca-alO&t=40"),
    BeadLocation("Chained Ogre", "Ashina Outskirts", BOSS, 6710, notes="#2", video="https://youtu.be/TfuiIJTFjg8?si=WjqL_d12jkJEM6eI&t=52"),
    BeadLocation("Samurai General Tenzen Yamauchi", "Ashina Outskirts", BOSS, 6762, notes="#3", video="https://youtu.be/TfuiIJTFjg8?si=C7v2f78NM9Ej2sHw&t=61"),
    BeadLocation("Blazing Bull", "Ashina Outskirts", BOSS, 6711, notes="#5", video="https://youtu.be/TfuiIJTFjg8?si=pvi2WSNdAV8LDRbB&t=85"),
    BeadLocation("Shinobi Hunter Enshin of Misen", "Hirata Estate", BOSS, 6763, notes="#6", video="https://youtu.be/TfuiIJTFjg8?si=dXvA0D7Ru7pGNm34&t=95"),
    BeadLocation("Juzuo the Drunkard ", "Hirata Estate", BOSS, 6764, notes="#7", video="https://youtu.be/TfuiIJTFjg8?si=o5GDfWtvitbsgnZa&t=106"),
    BeadLocation("Lone Shadow Swordsman - Depths Cave", "Ashina Castle", BOSS, 6770, notes="#9", video="https://youtu.be/TfuiIJTFjg8?si=FUg6wEUXMwHGvwo4&t=173"),
    BeadLocation("Seven Spears Shikibu Toshikatsu", "Ashina Castle", BOSS, 6769, notes="#10", video="https://youtu.be/TfuiIJTFjg8?si=8A_6oDStOOtzRSXk&t=150"),
    BeadLocation("Samurai General Kuramosuke Matsumoto", "Ashina Castle", BOSS, 6766, notes="#11", video="https://youtu.be/TfuiIJTFjg8?si=tbEZZW15WiLvMEld&t=135"),
    BeadLocation("Ashina Elite Jinsuke Saze", "Ashina Castle", BOSS, 6767, notes="#13", video="https://youtu.be/TfuiIJTFjg8?si=65OZhG-82_rpvvLv&t=202"),
    BeadLocation("Snake Eyes - Gun Fort", "Sunken Valley", BOSS, 6773, notes="#16", video="https://youtu.be/TfuiIJTFjg8?si=A533x05OW08t7we6&t=265"),
    BeadLocation("Long-Armed Centipede Giraffe", "Sunken Valley", BOSS, 6774, notes="#17", video="https://youtu.be/TfuiIJTFjg8?si=GED7ocsqLRk_fQqX&t=277"),
    BeadLocation("Armored Warrior", "Senpou Temple", BOSS, 6715, notes="#19", video="https://youtu.be/TfuiIJTFjg8?si=ARtxeCFQwgpgu-Q4&t=440"),
    BeadLocation("Long-Armed Centipede Sen'un", "Senpou Temple", BOSS, 6772, notes="#20", video="https://youtu.be/TfuiIJTFjg8?si=_-cuhqPY3OLGYwZ-&t=467"),
    BeadLocation("Snake Eyes Shirafuji", "Ashina Depths", BOSS, 6775, notes="#23", video="https://youtu.be/TfuiIJTFjg8?si=sjIKzfEFOJclFSNI&t=310"),
    BeadLocation("Dual Ape - Bead Drop 1", "Ashina Depths", BOSS, 6798, notes="#24", video="https://youtu.be/TfuiIJTFjg8?si=t-ZgKQYgecYK06Oq&t=353"),
    BeadLocation("Dual Ape - Bead Drop 2", "Ashina Depths", BOSS, 6799, notes="#25", video="https://youtu.be/TfuiIJTFjg8?si=t-ZgKQYgecYK06Oq&t=353"),
    BeadLocation("Tojujiro the Glutton - Hidden Forest", "Ashina Depths", BOSS, 6776, notes="#26", video="https://youtu.be/TfuiIJTFjg8?si=HQl5sCLI6TqWTw_Q&t=368"),
    BeadLocation("O'rin of the Water", "Ashina Depths", BOSS, 6777, notes="#27", video="https://youtu.be/TfuiIJTFjg8?si=lutATcKJD1NPOkx8&t=388"),
    BeadLocation("Chained Ogre Antechamber", "Ashina Castle (Dusk)", BOSS, 6778, notes="#30", video="https://youtu.be/TfuiIJTFjg8?si=wqQX7Uom0zFMyAhH&t=480"),
    BeadLocation("Lone Shadow Masanaga the Spear Bearer", "Ashina Castle (Dusk)", BOSS, 6780, notes="#31", video="https://youtu.be/TfuiIJTFjg8?si=Sloy-5i807mzVAgJ&t=538"),
    BeadLocation("Lone Shadow Vilehand - Upper Dojo", "Ashina Castle (Dusk)", BOSS, 6779, notes="#32", video="https://youtu.be/TfuiIJTFjg8?si=Di9Qcng-lcIaPt2V&t=492"),
    BeadLocation("Lone Shadow Masanaga - Past", "Hirata Estate (Owls Memory)", BOSS, 6781, notes="#33", video="https://youtu.be/TfuiIJTFjg8?si=YdN_KLL3RUEOXGOl&t=518"),
    BeadLocation("Juzou the Drunkard - Past", "Hirata Estate (Owls Memory)", BOSS, 6782, notes="#34", video="https://youtu.be/TfuiIJTFjg8?si=wbRMYw0-HjOiyH52&t=529"),
    BeadLocation("Sakura Bull of the Palace", "Fountainhead Palace", BOSS, 6783, notes="#35", video="https://youtu.be/TfuiIJTFjg8?si=Zqy2yUtf7CXIhNcn&t=552"),
    BeadLocation("Okami Leader Shizu", "Fountainhead Palace", BOSS, 6784, notes="#36", video="https://youtu.be/TfuiIJTFjg8?si=Q_V5foS1nvLpkvgZ&t=572"),
    BeadLocation("Red-Eyes Ashina Elite", "Ashina Castle (Night)", BOSS, 6785, notes="#38", video="https://youtu.be/TfuiIJTFjg8?si=Avld3QFcyLnA5Z7v&t=604"),
    BeadLocation("Shigekichi of the Red Guard - Drunkard", "Ashina Castle  (Night)", BOSS, 6787, notes="#39", video="https://youtu.be/TfuiIJTFjg8?si=Vc1v-o96AGy1dpXE&t=622"),
    BeadLocation("Seven Ashina Spears - Ashina Reservoir", "Ashina Castle (Night)", BOSS, 6786, notes="#40", video="https://youtu.be/TfuiIJTFjg8?si=t6Ncu6rjqHX58P_u&t=646"),

    # --------------------------
    # Vendors
    # --------------------------
    BeadLocation("Dungeon Entrance Merchent", "Ashina Castle", SHOP, 6768, notes="#14", video="https://youtu.be/TfuiIJTFjg8?si=DN2-FxRuILKLaZ_Q&t=213"),
]
# fmt: on


def get_bead_state(slot_data: bytes) -> list[dict]:
    return flag_state(PRAYER_BEADS, slot_data)
