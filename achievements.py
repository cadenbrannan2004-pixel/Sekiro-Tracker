
from bead_map import get_bead_state
from gourd_map import get_gourd_state
from prosthetic_map import get_prosthetic_state, get_prosthetic_upgrades, get_prosthetic_videos
from quantity_targets import get_quantity_state


def build_report(slot_data: bytes) -> dict:
    owned = get_prosthetic_state(slot_data)
    return {
        "prayer_beads": get_bead_state(slot_data),
        "gourd_seeds": get_gourd_state(slot_data),
        "prosthetic_tools": {
            "owned": owned,
            "missing": [name for name, has in owned.items() if not has],
            "upgrades": get_prosthetic_upgrades(slot_data),
            "videos": get_prosthetic_videos(),
        },
        "quantity_targets": get_quantity_state(slot_data),
    }
