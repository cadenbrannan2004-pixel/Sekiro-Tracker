
# Sekiro Achievement Tracker

A Python tool that reads Sekiro: Shadows Die Twice's save file directly and automatically tracks progress toward 100% completion — prayer beads, skills, prosthetic tools, boss memories, and key resources.

Built as a personal project to learn binary file reverse-engineering, game save formats, and full-stack Python development.

## What it does

Sekiro doesn't have a built-in completion tracker, and many collectibles such as Prayer Beads share a single stackable item type in-game, making it impossible to tell which of the 40 locations you've actually visited just by checking your inventory. This tool solves that by reading the save file's low-level *event flags* system which fires once an item is collected or purchased. 

It tracks:
- **Prayer Beads** (40 locations, grouped by region and source: boss drop, treasure, or shop purchase)
- **Skills** (grouped by skill tree)
- **Prosthetic Tools** (all 9 base tools)
- **Boss Memories** (all 14 major bosses, tracked through inventory rather than flags)
- **Key resources** (e.g. Lapis Lazuli, with configurable target thresholds)
- **Endings** (manually checked off since these are one-off story choices rather than something worth automating)

## How it works

Sekiro's PC save (`S0000.sl2`) is a proprietary binary container shared across FromSoftware's Souls-family engine. This project:

1. **Parses the save container** — splits it into its 10 individual character save slots
2. **Reads confirmed inventory offsets** (ported from community save-editor research) to check owned items, weapons, and goods quantities directly
3. **Reads a self discovered event flag table** — found empirically by diffing before/after save snapshots around known item pickups — to determine one-time pickup states that aren't reflected in inventory alone
4. **Cross-references flag IDs** captured live via [SoulSplitter](https://github.com/FrankvdStam/SoulSplitter)'s event flag logger while playing, mapping each one to a specific named location
5. **Serves the result** two ways: a headless watch loop that writes a JSON snapshot on every save change, or a local Flask dashboard with a live-updating, save-slot-aware web UI

No game files are modified. Everything is read-only.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```bash
uv venv --python 3.12
uv add flask
```

## Usage

**Sanity-check everything first:**
```bash
uv run test_connection.py
```

**Run the headless tracker** (writes `achievement_state.json` on every save change):
```bash
uv run tracker.py
```

**Or run the web dashboard:**
```bash
uv run webapp.py
```
Then open `http://localhost:5000`.

## Status

Prayer bead and skill flag IDs are discovered incrementally through my own playthroughs, using SoulSplitter's live event flag logger combined with save-file diffing. See `bead_map.py` and `skill_map.py` for current mapping progress or unmapped entries report `null`. Also the working on a frontend/gui.


## Prayer Bead Event-Flag Google Sheet:
https://docs.google.com/spreadsheets/d/17YkjiKnKZTHUHFSkf_SZK5KQrgrUO5_V1XxE4lfPpLA/edit?gid=0#gid=0


## Credits

- Save file container structure adapted from [alfizari/Sekiro-Save-Editor](https://github.com/alfizari/Sekiro-Save-Editor)
- Event flag discovery informed by [SoulSplitter](https://github.com/FrankvdStam/SoulSplitter)'s wiki and live logger tooling
