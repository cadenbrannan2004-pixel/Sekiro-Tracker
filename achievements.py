"""
achievements.py

Combines every tracked achievement category into one report. This is
what tracker.py should call instead of talking to bead_map directly.
"""

from bead_map import get_bead_state
from gourd_map import get_gourd_state
from prosthetic_map import get_prosthetic_state
from quantity_targets import get_quantity_state


def build_report(slot_data: bytes) -> dict:
    owned = get_prosthetic_state(slot_data)
    return {
        "prayer_beads": get_bead_state(slot_data),
        "gourd_seeds": get_gourd_state(slot_data),
        "prosthetic_tools": {
            "owned": owned,
            "missing": [name for name, has in owned.items() if not has],
        },
        "quantity_targets": get_quantity_state(slot_data),
    }
