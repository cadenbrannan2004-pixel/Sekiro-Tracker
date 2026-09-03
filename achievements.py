"""
achievements.py

Combines every tracked achievement category into one report. This is
what tracker.py should call instead of talking to bead_map directly.
"""

from bead_map import get_bead_state
from skill_map import get_skill_state
from prosthetic_map import get_prosthetic_state, missing_prosthetics
from quantity_targets import get_quantity_state


def build_report(slot_data: bytes) -> dict:
    return {
        "prayer_beads": get_bead_state(slot_data),
        "skills": get_skill_state(slot_data),
        "prosthetic_tools": {
            "owned": get_prosthetic_state(slot_data),
            "missing": missing_prosthetics(slot_data),
        },
        "quantity_targets": get_quantity_state(slot_data),
    }
