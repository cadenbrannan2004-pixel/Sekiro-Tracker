"""
gourd_map.py

Gourd Seed pickup locations

"""

from bead_map import BOSS, CHEST, PICKUP, SHOP, BeadLocation as GourdLocation
from event_flags import flag_state


# Grouped by how it's obtained, route order within each group; flag None = not mapped yet.
# fmt: off
GOURD_SEEDS: list[GourdLocation] = [
    # --------------------------
    # Pickups / Chests
    # --------------------------
    GourdLocation("Outskirts Stairway Idol", "Ashina Outskirts", PICKUP, 6725, video=""),
    GourdLocation("Upper Tower Antechamber Chest", "Ashina Castle", CHEST, video=""),
    GourdLocation("Praying Monks Feet", "Senpou Temple", PICKUP, video=""),
    GourdLocation("Gun Fort Hut", "Sunken Valley", PICKUP, video=""),
    GourdLocation("Canopy Tree", "Mibu Village", PICKUP, video=""),
    GourdLocation("Palace Grounds Large Chest", "Fountainhead Palace", CHEST, 6729, video=""),

    # --------------------------
    # Boss Drops
    # --------------------------
    GourdLocation("Naomori Kawarada Seed Drop", "Ashina Outskirts - Gate Path", BOSS, 6760, video=""),

    # --------------------------
    # Vendors
    # --------------------------
    GourdLocation("Battlefield Memorial Mob Vendor", "Ashina Outskirts", SHOP, video=""),
    GourdLocation("Fujioka the Info Broker", "Temple", SHOP, 6722, video=""),
]
# fmt: on


def get_gourd_state(slot_data: bytes) -> list[dict]:
    return flag_state(GOURD_SEEDS, slot_data)
