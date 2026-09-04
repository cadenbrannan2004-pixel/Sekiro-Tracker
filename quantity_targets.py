"""
quantity_targets.py

For achievement-relevant items where progress is a COUNT rather than a
picked-up/not-picked-up state -- e.g. Lapis Lazuli, needed in specific
amounts to unlock certain endgame purchases. No flag table needed; this
reuses the same confirmed inventory offsets as prosthetic_map.py.
"""

from dataclasses import dataclass


@dataclass
class QuantityTarget:
    name: str
    item_id: int
    target: int  # how many you actually need for the relevant achievement/purchase


QUANTITY_TARGETS: list[QuantityTarget] = [
    QuantityTarget("Lapis Lazuli", 6400, target = 10),  # set target to whatever you're tracking toward
    QuantityTarget("Treasure Carp Scale", 10000, target = 42),  
    QuantityTarget("Shinobi Esoteric Text", 2920, target = 1), 
    QuantityTarget("Prosthetic Esoteric Text", 2921, target = 1),
    QuantityTarget("Ashina Esoteric Text", 2922, target = 1),
    QuantityTarget("Senpou Esoteric Text", 2923, target = 1), 
    QuantityTarget("Mushin Esoteric Text", 2924, target = 1),
]


def get_quantity_state(slot_data: bytes) -> dict[str, dict]:
    from inventory_reader import get_good_quantity

    result = {}
    for item in QUANTITY_TARGETS:
        have = get_good_quantity(slot_data, item.item_id)
        result[item.name] = {
            "have": have,
            "target": item.target,
            "complete": have >= item.target,
        }
    return result
