

# Sekiro Achievement Tracker

A Python tool that reads Sekiro: Shadows Die Twice's save file directly and automatically tracks progress toward 100% completion(prayer beads, prosthetic tools, boss memories, and key resources).

Built as a personal project to learn binary file reverse-engineering, game save formats, and full-stack Python development.

## What it does

Sekiro doesn't have a built-in completion tracker, and many collectibles (like Prayer Beads) share a single stackable item type in-game, making it impossible to tell which of the 40 locations you've actually visited just by checking your inventory. This tool solves that by reading the save file's event flags.

It tracks:
- **Prayer Beads** (40 locations, grouped by region and source: boss drop, treasure, or shop purchase)
- **Skills** (grouped by skill tree)
- **Prosthetic Tools** (all 9 base tools)
- **Boss Memories** (all 14 major bosses, tracked via inventory rather than flags)
- **Key resources** (e.g. Lapis Lazuli, with configurable target thresholds)
- **Endings** (manually checked off, since these are one-off story choices rather than something worth automating)

## How it works

Sekiro's PC save (`S0000.sl2`) is a proprietary binary container shared across FromSoftware's Souls engine. This project:

1. **Parses the save container** splits it into its 10 individual character save slots
2. **Reads confirmed inventory offsets** (ported from community save-editor research) to check owned items, weapons, and goods quantities directly
3. **Reads a custom-discovered event flag table** found empirically by diffing before/after save snapshots around known item pickups to determine one-time pickup states that aren't reflected in inventory alone
4. **Cross-references flag IDs** captured live via [SoulSplitter](https://github.com/FrankvdStam/SoulSplitter)'s event flag logger while playing, mapping each one to a specific named location
5. **Serves the result** two ways: a headless watch loop that writes a JSON snapshot on every save change, or a local Flask dashboard with live-updating

No game files are modified. Everything is read-only

## Status

Prayer bead and skill flag IDs are discovered incrementally through manual play, using SoulSplitter's live event flag logger combined with save-file diffing. See `bead_map.py` and `skill_map.py` for current mapping progress or unmapped entries report `null`. Also working to learn the frontend/gui portion through ai-assistance and other media options. 

# Google Sheet for all triggered event flags for each prayer bead drop in the game: 

https://docs.google.com/spreadsheets/d/17YkjiKnKZTHUHFSkf_SZK5KQrgrUO5_V1XxE4lfPpLA/edit?gid=0#gid=0

## Credits

- Save file container structure adapted from [alfizari/Sekiro-Save-Editor](https://github.com/alfizari/Sekiro-Save-Editor)
- Event flag discovery informed by [SoulSplitter](https://github.com/FrankvdStam/SoulSplitter)'s wiki and live logger tooling
