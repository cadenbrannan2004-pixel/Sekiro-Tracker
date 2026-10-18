"""
gourd_map.py

Gourd Seed pickup locations

"""

from bead_map import BeadLocation as GourdLocation
from event_flags import flag_state


GOURD_SEEDS: list[GourdLocation] = [
    GourdLocation("Naomori Kawarada Seed Drop", "Ashina Outskirts - Gate Path", event_flag_id=6760, notes="#1"),
    GourdLocation("Outskirts Stairway Idol", "Ashina Outskirts", event_flag_id=6725, notes="#2"),
    GourdLocation("Battlefield Memorial Mob Vendor", "Ashina Outskirts", event_flag_id=None, notes="#3"),
    GourdLocation("Upper Tower Antechamber Chest", "Ashina Castle", event_flag_id=None, notes="#4"),
    GourdLocation("Fujioka the Info Broker", "Temple", event_flag_id=None, notes="#5"),
    GourdLocation("Praying Monks Feet", "Senpou Temple", event_flag_id=None, notes="#6"),
    GourdLocation("Gun Fort Hut", "Sunken Valley", event_flag_id=None, notes="#7"),
    GourdLocation("Mibu VillageCanopy Tree", "Mibu Village", event_flag_id=None, notes="#8"),
    GourdLocation("Palace Grounds Large Chest", "Fountainhead Palace", event_flag_id=None, notes="#9"),
]


def get_gourd_state(slot_data: bytes) -> dict[str, bool | None]:
    return flag_state(GOURD_SEEDS, slot_data)
