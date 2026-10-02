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


ENDINGS: list[Ending] = [
    # Still needs updating 
    Ending("return", "Return Ending (Dragon's Homecoming)", [
        EndingRequirement("return_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("return_no_shura", "Have not triggered the Shura path"),
        EndingRequirement("return_no_frozen_tears", "Have not obtained Frozen Tears (locks Purification/Immortal Severance)"),
        EndingRequirement("return_isshin", "Defeated Isshin, the Sword Saint"),
        EndingRequirement("return_choice", "Chose to let Kuro live at the final dialogue"),
    ]),
    Ending("purification", "Purification Ending", [
        EndingRequirement("severance_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("shura_trigger", "Collected Lotus of the Palace, Shelter Stone, and Mortal Blade"),
        EndingRequirement("purification_frozen_tears", "Obtained Tomoe's Note and speak to Emma at the Old Grave Idol"),
        EndingRequirement("purification_gyoubu_reward", "Obtained Father's Bell Charm and Defeated Owl (Father)"),
        EndingRequirement("purification_final_boss", "Defeated Isshin, the Sword Saint"),
        EndingRequirement("purification_final_boss", "Gave Kuro Aromatic Flower and Divine Dragon's Tears"),
    ]),
    Ending("immortal_severance", "Immortal Severance Ending", [
        EndingRequirement("severance_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("shura_trigger", "Collected Lotus of the Palace, Shelter Stone, and Mortal Blade"),
        EndingRequirement("severance_choice", "Speak to Owl and chose to stay loyal to Kuro"),
        EndingRequirement("severance_final_boss", "Defeated Isshin, the Sword Saint"),
        EndingRequirement("severance_final_boss", "Give Kuro only the Divine Dragon Tears"),
    ]),
    Ending("shura", "Shura Ending", [
        EndingRequirement("severance_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("shura_trigger", "Collected Lotus of the Palace and Shelter Stone"),
        EndingRequirement("shura_trigger", "Speak to Owl and chose the Shura path through the Iron Code"),
        EndingRequirement("shura_final_boss", "Defeated Emma and Isshin Ashina"),
    ]),
]
