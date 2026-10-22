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
    ProstheticTool("Loaded Shuriken", 70000, video="https://youtu.be/1tH0061_VO4?si=hdUNu3CXnqtD060p&t=10"),
    ProstheticTool("Shinobi Firecracker", 71000, video="https://youtu.be/1tH0061_VO4?si=mAs9WERq05_dzZ-o&t=103"),
    ProstheticTool("Flame Vent", 72000, video="https://youtu.be/1tH0061_VO4?si=qBvbrElTUcUApAzI&t=175"),
    ProstheticTool("Loaded Axe", 73000, video="https://youtu.be/1tH0061_VO4?si=ssc1lGzcv9EKqJ1w&t=225"),
    ProstheticTool("Mist Raven", 74000, video="https://youtu.be/1tH0061_VO4?si=4oWmPPB2whKIcAK-&t=315"),
    ProstheticTool("Sabimaru", 75000, video="https://youtu.be/1tH0061_VO4?si=5KyvS1C-CHax5BRp&t=582"),
    ProstheticTool("Loaded Umbrella", 76000, video="https://youtu.be/1tH0061_VO4?si=s7f61rx-HtFOHLwJ&t=647"),
    ProstheticTool("Divine Abduction", 77000, video="https://youtu.be/1tH0061_VO4?si=-UfGUqnFhxW02H7N&t=726"),
    ProstheticTool("Loaded Spear", 78000, video="https://youtu.be/1tH0061_VO4?si=rj7BLp3-UZYPymHj&t=423"),
    ProstheticTool("Finger Whistle", 79000, video="https://youtu.be/1tH0061_VO4?si=bd2ImzhXB0-nLGQv&t=789"),
    
]


def get_prosthetic_state(slot_data: bytes) -> dict[str, bool]:
    return {tool.name: owns_weapon(slot_data, tool.item_id) for tool in PROSTHETIC_TOOLS}


def get_prosthetic_videos() -> dict[str, str]:
    return {tool.name: tool.video for tool in PROSTHETIC_TOOLS}
