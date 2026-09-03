"""
skill_map.py

Skills (Shinobi Arts, Prosthetic Arts, and the various combat style
trees) are the one category here that isn't inventory-based. They almost
certainly work like prayer beads did before you'd mapped them: a
"learned/not learned" bit per skill.

Two possibilities worth testing, in order of likelihood:
  1. Skills share the SAME flag table as world pickups (prayer beads,
     key items, etc.) -- in which case, once event_flags.FLAG_TABLE_OFFSET
     is confirmed, you just need to find the right flag_id per skill.
  2. Skills live in a separate table entirely -- in which case repeat the
     event_flags.find_flag_table_offset() diffing process, but trigger the
     change by learning a skill (spend skill points on it) instead of
     picking up an item.

Either way, the mechanism in event_flags.py should work unchanged --
you're just potentially pointing it at a different table_offset.
"""

from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    tree: str  # e.g. "Shinobi Arts", "Prosthetic Arts", "Ashina Style"
    event_flag_id: int | None = None
    table_offset: int | None = None  # override if skills use a different table than beads


# Seed list -- fill in as you confirm flag IDs. This is NOT exhaustive;
# Sekiro has dozens of skills across several trees.
SKILLS: list[Skill] = [
    Skill("Mikiri Counter", "Ashina Style"),
    Skill("Whirlwind Slash", "Ashina Style"),
    Skill("Ichimonji", "Ashina Style"),
    Skill("Shadowrush", "Shinobi Arts"),
    Skill("Shadowfall", "Shinobi Arts"),
    Skill("Sakura Dance", "Prosthetic Arts"),
    # ... continue for the rest.
]


def get_skill_state(slot_data: bytes) -> dict[str, bool | None]:
    from event_flags import read_flag

    result = {}
    for skill in SKILLS:
        if skill.event_flag_id is None:
            result[skill.name] = None
            continue
        result[skill.name] = read_flag(slot_data, skill.event_flag_id, skill.table_offset)
    return result
