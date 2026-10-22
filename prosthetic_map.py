"""
prosthetic_map.py

Base prosthetic tools (the 8 core tools, ignoring their upgrade variants
which are just alternate item_ids for the same tool once upgraded at the
Sculptor). IDs confirmed from alfizari's weapons.json.

"""

from dataclasses import dataclass

from inventory_reader import owns_weapon


@dataclass
class ProstheticTool:
    name: str
    item_id: int
    video: str = ""  # YouTube links


PROSTHETIC_TOOLS: list[ProstheticTool] = [
    ProstheticTool("Loaded Shuriken", 70000, video=""),
    ProstheticTool("Shinobi Firecracker", 71000, video=""),
    ProstheticTool("Flame Vent", 72000, video=""),
    ProstheticTool("Loaded Axe", 73000, video=""),
    ProstheticTool("Mist Raven", 74000, video=""),
    ProstheticTool("Sabimaru", 75000, video=""),
    ProstheticTool("Loaded Umbrella", 76000, video=""),
    ProstheticTool("Divine Abduction", 77000, video=""),
    ProstheticTool("Loaded Spear", 78000, video=""),
    ProstheticTool("Finger Whistle", 79000, video=""),
    
]


def get_prosthetic_state(slot_data: bytes) -> dict[str, bool]:
    return {tool.name: owns_weapon(slot_data, tool.item_id) for tool in PROSTHETIC_TOOLS}


def get_prosthetic_videos() -> dict[str, str]:
    return {tool.name: tool.video for tool in PROSTHETIC_TOOLS}
