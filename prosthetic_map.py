"""
prosthetic_map.py

Base prosthetic tools (the 8 core tools, ignoring their upgrade variants
which are just alternate item_ids for the same tool once upgraded at the
Sculptor). IDs confirmed from alfizari's weapons.json.

If you want to track SPECIFIC upgrade paths too (e.g. "do I have the
Lazulite Axe specifically") rather than just "do I have some version of
the Axe," add those ids as separate ProstheticTool entries -- ownership
of ANY variant id under the same base tool usually implies you unlocked
the base tool at minimum.
"""

from dataclasses import dataclass


@dataclass
class ProstheticTool:
    name: str
    item_id: int


PROSTHETIC_TOOLS: list[ProstheticTool] = [
    ProstheticTool("Loaded Shuriken", 70000),
    ProstheticTool("Shinobi Firecracker", 71000),
    ProstheticTool("Flame Vent", 72000),
    ProstheticTool("Loaded Axe", 73000),
    ProstheticTool("Mist Raven", 74000),
    ProstheticTool("Sabimaru", 75000),
    ProstheticTool("Loaded Umbrella", 76000),
    ProstheticTool("Loaded Spear", 78000),
    ProstheticTool("Finger Whistle", 79000),
]


def get_prosthetic_state(slot_data: bytes) -> dict[str, bool]:
    from inventory_reader import owns_weapon

    return {tool.name: owns_weapon(slot_data, tool.item_id) for tool in PROSTHETIC_TOOLS}


def missing_prosthetics(slot_data: bytes) -> list[str]:
    state = get_prosthetic_state(slot_data)
    return [name for name, owned in state.items() if not owned]
