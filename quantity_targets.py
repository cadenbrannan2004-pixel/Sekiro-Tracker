"""
quantity_targets.py

For achievement-relevant items where progress is a COUNT rather than a
picked-up/not-picked-up state
"""

from dataclasses import dataclass

from inventory_reader import get_good_quantity


@dataclass
class QuantityTarget:
    name: str
    item_id: int
    target: int  # how many you actually need for the relevant achievement/purchase
    checkbox: bool = False  # one-per-save items: show held/not-held instead of a bar
    video: str = ""  # YouTube links


QUANTITY_TARGETS: list[QuantityTarget] = [
    # set targets to whatever   
    QuantityTarget("Lapis Lazuli", 6400, target = 10, video=""),  
    QuantityTarget("Treasure Carp Scale", 10000, target = 42, video=""),  
    QuantityTarget("Shinobi Esoteric Text", 2920, target = 1, checkbox=True, video="https://youtu.be/aH-lHErhCjI?si=I6hQ8qhasIwkqHmt&t=40"), 
    QuantityTarget("Prosthetic Esoteric Text", 2921, target = 1, checkbox=True, video="https://youtu.be/aH-lHErhCjI?si=JrDBnPV5fDf3dYLA&t=69"),
    QuantityTarget("Ashina Esoteric Text", 2922, target = 1, checkbox=True, video="https://youtu.be/aH-lHErhCjI?si=OYdEv5QA1tCos6dK&t=98"),
    QuantityTarget("Senpou Esoteric Text", 2923, target = 1, checkbox=True, video="https://youtu.be/aH-lHErhCjI?si=3aZ83BOyqgvd2OcA&t=199"), 
    QuantityTarget("Mushin Esoteric Text", 2924, target = 1, checkbox=True, video="https://youtu.be/aH-lHErhCjI?si=xXiXrjFBS-XOPr_P&t=248"),
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
            "video": item.video,
        }
    return result
