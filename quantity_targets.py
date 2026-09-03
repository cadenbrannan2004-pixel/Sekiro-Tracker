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
    QuantityTarget("Lapis Lazuli", 6400, target=999),  # set target to whatever you're tracking toward
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
