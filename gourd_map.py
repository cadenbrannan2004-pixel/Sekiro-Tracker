
from bead_map import BOSS, CHEST, PICKUP, SHOP, BeadLocation as GourdLocation
from event_flags import flag_state


# Grouped by how it's obtained, route order within each group; flag None = not mapped yet.
# fmt: off
GOURD_SEEDS: list[GourdLocation] = [
    # --------------------------
    # Pickups / Chests
    # --------------------------
    GourdLocation("Outskirts Stairway Idol", "Ashina Outskirts", PICKUP, 6725, video="https://youtu.be/UNumOeKDNDM?si=NaH5eR2Afyskl3Rb&t=21"),
    GourdLocation("Upper Tower Antechamber Chest", "Ashina Castle", CHEST, 6726, video="https://youtu.be/UNumOeKDNDM?si=ZZPmXMUOCwaKN3EU&t=68"),
    GourdLocation("Praying Monks Feet", "Senpou Temple", PICKUP, 6727, video="https://youtu.be/UNumOeKDNDM?si=pWrsZLYX4W3XEH1F&t=75"),
    GourdLocation("Gun Fort Hut", "Sunken Valley", PICKUP, 6724, video="https://youtu.be/UNumOeKDNDM?si=lmUoxhqZwINerzZ6&t=86"),
    GourdLocation("Canopy Tree", "Mibu Village", PICKUP, 6728, video="https://youtu.be/UNumOeKDNDM?si=Mu9TzvTuSjfyWgPz&t=104"),
    GourdLocation("Palace Grounds Large Chest", "Fountainhead Palace", CHEST, 6729, video="https://youtu.be/UNumOeKDNDM?si=MzHsEnfjKnK7AAEn&t=117"),

    # --------------------------
    # Boss Drops
    # --------------------------
    GourdLocation("Naomori Kawarada Seed Drop", "Ashina Outskirts - Gate Path", BOSS, 6760, video="https://youtu.be/UNumOeKDNDM?si=TcIq1W1ikQzBGjPX&t=8"),

    # --------------------------
    # Vendors
    # --------------------------
    GourdLocation("Battlefield Memorial Mob Vendor", "Ashina Outskirts", SHOP, 6721, video="https://youtu.be/UNumOeKDNDM?si=bupOvMhfQr-1XZUj&t=32"),
    GourdLocation("Fujioka the Info Broker", "Temple", SHOP, 6722, video="https://youtu.be/UNumOeKDNDM?si=2XZGDdzfJQ-SZgUJ&t=44"),
]
# fmt: on


def get_gourd_state(slot_data: bytes) -> list[dict]:
    return flag_state(GOURD_SEEDS, slot_data)
