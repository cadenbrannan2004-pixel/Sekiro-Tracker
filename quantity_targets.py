"""
quantity_targets.py

For achievement-relevant items where progress is a COUNT rather than a
picked-up/not-picked-up state -- e.g. Lapis Lazuli, needed in specific
amounts to unlock certain endgame purchases. No flag table needed; this
reuses the same confirmed inventory offsets as prosthetic_map.py.
"""

from dataclasses import dataclass

from inventory_reader import get_good_quantity


@dataclass
class QuantityTarget:
    name: str
    item_id: int
    target: int  # how many you actually need for the relevant achievement/purchase
    checkbox: bool = False  # one-per-save items: show held/not-held instead of a bar


QUANTITY_TARGETS: list[QuantityTarget] = [
    # set targets to whatever   
    QuantityTarget("Lapis Lazuli", 6400, target = 10),  
    QuantityTarget("Treasure Carp Scale", 10000, target = 42),  
    QuantityTarget("Shinobi Esoteric Text", 2920, target = 1, checkbox=True), 
    QuantityTarget("Prosthetic Esoteric Text", 2921, target = 1, checkbox=True),
    QuantityTarget("Ashina Esoteric Text", 2922, target = 1, checkbox=True),
    QuantityTarget("Senpou Esoteric Text", 2923, target = 1, checkbox=True), 
    QuantityTarget("Mushin Esoteric Text", 2924, target = 1, checkbox=True),
]


def get_quantity_state(slot_data: bytes) -> dict[str, dict]:
    result = {}
    for item in QUANTITY_TARGETS:
        have = get_good_quantity(slot_data, item.item_id)
        result[item.name] = {
            "have": have,
            "target": item.target,
            "complete": have >= item.target,
            "checkbox": item.checkbox,
        }
    return result
