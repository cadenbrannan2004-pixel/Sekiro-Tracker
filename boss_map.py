
from dataclasses import dataclass


@dataclass
class Boss:
    id: str  # key in boss_state.json for manual bosses
    name: str
    region: str
    achievement: str = ""  # Steam achievement this boss unlocks; blank = manual checkbox
    note: str = ""  # route requirement shown under the name
    video: str = ""  # YouTube links


SHURA_ONLY = "Shura ending only"
NOT_SHURA = "Not on the Shura route"

# fmt: off
REQUIRED_BOSSES: list[Boss] = [
    Boss("gyoubu", "Gyoubu Masataka Oniwa", "Ashina Outskirts", achievement="Gyoubu Masataka Oniwa"),
    Boss("lady_butterfly", "Lady Butterfly", "Hirata Estate", achievement="The Phantom Lady Butterfly"),
    Boss("genichiro", "Genichiro Ashina", "Ashina Castle", achievement="Genichiro Ashina"),
    Boss("folding_screen_monkeys", "Folding Screen Monkeys", "Senpou Temple", achievement="Folding Screen Monkeys"),
    Boss("guardian_ape", "Guardian Ape", "Sunken Valley", achievement="Guardian Ape"),
    Boss("corrupted_monk_ghost", "Corrupted Monk", "Ashina Depths"),
    Boss("headless_ape", "Headless Ape", "Ashina Depths"),
    Boss("great_shinobi_owl", "Great Shinobi Owl", "Ashina Castle", achievement="Great Shinobi - Owl"),
    Boss("owl_father", "Owl (Father)", "Hirata Estate (Owls Memory)", achievement="Father Surpassed", note="Needs Father's Bell Charm"),
    Boss("true_corrupted_monk", "True Corrupted Monk", "Fountainhead Palace", achievement="Corrupted Monk", note=NOT_SHURA),
    Boss("divine_dragon", "Divine Dragon", "Fountainhead Palace", achievement="Gracious Gift of Tears", note=NOT_SHURA),
    Boss("demon_of_hatred", "Demon of Hatred", "Ashina Outskirts", achievement="Demon of Hatred"),
    Boss("isshin_sword_saint", "Isshin, the Sword Saint", "Ashina Reservoir", achievement="Sword Saint, Isshin Ashina", note=NOT_SHURA),
    Boss("emma", "Emma, the Gentle Blade", "Ashina Castle", note=SHURA_ONLY),
    Boss("isshin_ashina", "Isshin Ashina", "Ashina Castle", achievement="Isshin Ashina", note=SHURA_ONLY),
]

HIDDEN_BOSSES: list[Boss] = [
    Boss("great_serpent", "Great Serpent", "Sunken Valley", achievement="Great Serpent",
         note="Needs Mortal Blade and Puppeteer Ninjutsu, kite route from Senpou Temple", video=""),
    Boss("great_colored_carp", "Great Colored Carp", "Fountainhead Palace", achievement="Great Colored Carp",
         note="Feed it Truly Precious Bait from a Pot Noble", video=""),
    Boss("guardian_ape_severed", "Guardian Ape (Mortal Blade)", "Sunken Valley", achievement="Guardian Ape Immortality Severed",
         note="Deathblow the ape's corpse with the Mortal Blade", video=""),
]
# fmt: on

MAN_WITHOUT_EQUAL = "Man Without Equal"
MANUAL_IDS = {boss.id for boss in REQUIRED_BOSSES + HIDDEN_BOSSES if not boss.achievement}


def _rows(bosses: list[Boss], achievements: dict[str, bool] | None, checked: dict[str, bool]) -> list[dict]:
    rows = []
    for boss in bosses:
        manual = not boss.achievement
        if manual:
            defeated = checked.get(boss.id, False)
        else:
            defeated = None if achievements is None else achievements.get(boss.achievement)
        rows.append({
            "id": boss.id,
            "name": boss.name,
            "region": boss.region,
            "achievement": boss.achievement,
            "note": boss.note,
            "video": boss.video,
            "manual": manual,
            "defeated": defeated,
        })
    return rows


def get_account_bosses(achievements: dict[str, bool] | None, checked: dict[str, bool]) -> dict:
    """achievements: from steam_achievements.read_achievements (None = unavailable).
    checked: this account's manual checkboxes from boss_state.json."""
    return {
        "steam_available": achievements is not None,
        "man_without_equal": None if achievements is None else achievements.get(MAN_WITHOUT_EQUAL),
        "required": _rows(REQUIRED_BOSSES, achievements, checked),
        "hidden": _rows(HIDDEN_BOSSES, achievements, checked),
    }


_ids = [boss.id for boss in REQUIRED_BOSSES + HIDDEN_BOSSES]
if len(_ids) != len(set(_ids)):
    raise ValueError("Duplicate boss id")
del _ids
