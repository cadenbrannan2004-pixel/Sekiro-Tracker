"""
endings.py

Manual checklist definitions for Sekiro's four endings. This is
intentionally a self-reported checklist, not auto-read state.

"""

from dataclasses import dataclass


@dataclass
class EndingRequirement:
    id: str
    text: str


@dataclass
class Ending:
    id: str
    name: str
    requirements: list[EndingRequirement]
    video: str = ""  # YouTube guide for the endings


ENDINGS: list[Ending] = [
    Ending("return", "Return Ending (Dragon's Homecoming)", [
        EndingRequirement("return_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("return_key_items", "Collected Holy Chapter: Infested, Lotus of the Palace, Shelter Stone, and Mortal Blade"),
        EndingRequirement("return_persimmon", "Gave the Divine Child the Persimmon and acquired Kuro's Rice"),
        EndingRequirement("return_sweet_rice_balls", "Acquired Sweet Rice Balls from Kuro "),
        EndingRequirement("return_illusory_hall", "Spoke to the Divine Child in Illusory Hall"),
        EndingRequirement("return_dragons_return", "Acquired Holy Chapter: Dragon's Return and gave it to Divine Child"),
        EndingRequirement("return_serpent_viscera", "Collected both Serpent Viscera and gave it to Divine Child"),
        EndingRequirement("return_frozen_tears", "Recieved Frozen Tears from Divine Child"),
        EndingRequirement("return_divine_dragon", "Defeated the Divine Dragon"),
        EndingRequirement("return_isshin", "Defeated Isshin, the Sword Saint"),
        EndingRequirement("return_choice", "Gave Kuro the Frozen Tears and Divine Dragon Tears"),
    ], video=""),
    Ending("purification", "Purification Ending", [
        EndingRequirement("purification_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("purification_key_items", "Collected Lotus of the Palace, Shelter Stone, and Mortal Blade"),
        EndingRequirement("purification_tomoes_note", "Obtained Tomoe's Note and speak to Emma at the Old Grave Idol"),
        EndingRequirement("purification_owl_father", "Obtained Father's Bell Charm and Defeated Owl (Father)"),
        EndingRequirement("purification_isshin", "Defeated Isshin, the Sword Saint"),
        EndingRequirement("purification_choice", "Gave Kuro Aromatic Flower and Divine Dragon's Tears"),
    ], video=""),
    Ending("immortal_severance", "Immortal Severance Ending", [
        EndingRequirement("severance_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("severance_key_items", "Collected Lotus of the Palace, Shelter Stone, and Mortal Blade"),
        EndingRequirement("severance_choice", "Speak to Owl and chose to stay loyal to Kuro"),
        EndingRequirement("severance_isshin", "Defeated Isshin, the Sword Saint"),
        EndingRequirement("severance_final_choice", "Gave Kuro only the Divine Dragon Tears"),
    ], video=""),
    Ending("shura", "Shura Ending", [
        EndingRequirement("shura_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("shura_key_items", "Collected Lotus of the Palace and Shelter Stone"),
        EndingRequirement("shura_trigger", "Spoke to Owl and chose the Shura path through the Iron Code"),
        EndingRequirement("shura_final_boss", "Defeated Emma and Isshin Ashina"),
    ], video=""),
]


_seen_ids: set[str] = set()
for _ending in ENDINGS:
    for _req in _ending.requirements:
        if _req.id in _seen_ids:
            raise ValueError(f"Duplicate ending requirement id: {_req.id!r}")
        _seen_ids.add(_req.id)
del _seen_ids
