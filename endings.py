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
    Ending("return", "Return", [
        EndingRequirement("return_no_shura", "Have not triggered the Shura path"),
        EndingRequirement("return_no_frozen_tears", "Have not obtained Frozen Tears (locks Purification/Immortal Severance)"),
        EndingRequirement("return_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("return_isshin", "Defeated Isshin, the Sword Saint"),
        EndingRequirement("return_choice", "Chose to let Kuro live at the final dialogue"),
    ]),
    Ending("purification", "Purification (Age of the Dragon Reborn)", [
        EndingRequirement("purification_frozen_tears", "Obtained Frozen Tears from Emma"),
        EndingRequirement("purification_gyoubu_reward", "Gave Frozen Tears to Kuro"),
        EndingRequirement("purification_divine_heir", "Progressed the Divine Heir substitute questline"),
        EndingRequirement("purification_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("purification_final_boss", "Defeated Isshin, the Sword Saint / Inner Isshin (Purification variant)"),
    ]),
    Ending("immortal_severance", "Immortal Severance", [
        EndingRequirement("severance_frozen_tears", "Obtained Frozen Tears from Emma"),
        EndingRequirement("severance_iron_code", "Read all 3 volumes of the Iron Code text"),
        EndingRequirement("severance_choice", "Chose the Immortal Severance dialogue option with Kuro"),
        EndingRequirement("severance_genichiro", "Defeated Genichiro, Way of Tomoe (rooftop)"),
        EndingRequirement("severance_final_boss", "Defeated Isshin, the Sword Saint / Inner Isshin (Severance variant)"),
    ]),
    Ending("shura", "Shura", [
        EndingRequirement("shura_trigger", "Triggered the Shura path (resurrection-heavy playstyle / specific early dialogue)"),
        EndingRequirement("shura_no_emma", "Did not give Frozen Tears to Kuro"),
        EndingRequirement("shura_genichiro", "Defeated Genichiro, Way of Tomoe (Shura variant fight)"),
        EndingRequirement("shura_final_boss", "Defeated Isshin Ashina (young, Shura variant)"),
    ]),
]
