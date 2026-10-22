

WARNING: In-progress project but near the end of the development. Download added but urls still need to be added before I publish anything rn.

# Sekiro Achievement Tracker

> **Beta:** ready for testing. If something looks wrong, please [open an issue](https://github.com/cadenbrannan2004-pixel/Sekiro-Tracker/issues).
 
A Python tool that reads Sekiro: Shadows Die Twice's save file directly and automatically tracks progress toward 100% completion(prayer beads, prosthetic tools, endings, and key resources (lapis and carp scales)).

Built as a personal project!

## What it does

Sekiro doesn't have a built-in completion tracker, and many collectibles (like Prayer Beads and gourd seeds) share a single stackable item type in-game, making it impossible to tell which of the 40 locations you've actually visited just by checking your inventory. This tool solves that by reading the save file's event flags.

## Download and run
 
1. Go to the [latest release](https://github.com/cadenbrannan2004-pixel/Sekiro-Tracker/releases/latest) and download `SekiroTracker.exe`.
2. Put it in its own folder (for example `Documents\SekiroTracker`). It saves your ending checklist next to itself.
3. Double-click `SekiroTracker.exe`. A small console window opens, then your dashboard opens in your browser.
4. Play the game. The dashboard updates every time Sekiro saves (resting at an idol, picking things up, quitting to the menu).
**To close it:** close the dashboard tab (the tracker shuts down a few seconds later), or close the console window.
 
### "Windows protected your PC"
 
The app isn't code-signed, so Windows SmartScreen may warn you the first time. Click **More info**, then **Run anyway**. The full source code is in this repository if you want to check what it does!
 
## Requirements
 
- Windows PC with Sekiro: Shadows Die Twice on Steam
- The game has saved at least once (your save is found automatically at `%APPDATA%\Sekiro\<your Steam ID>\S0000.sl2`)
- Tested on game version 1.06

It tracks:
- **Prayer Beads** (40 locations, grouped by region and source: boss drop, treasure, or shop purchase)
- **Prosthetic Tools** (all 10 base tools)
- **Endings** (all 4 endings with a manual checklist to keep track of where youre at)
- **Key resources** (for example Lapis Lazuli, with configurable target thresholds)

## How it works

Sekiro's PC save (`S0000.sl2`) is a proprietary binary container shared across FromSoftware's Souls engine:

1. **Parses the save container** splits it into its 10 individual character save slots
2. **Reads confirmed inventory offsets** (ported from community save-editor research) to check owned items, weapons, and goods quantities directly
3. **Reads a custom-discovered event flag table** found empirically by diffing before/after save snapshots around known item pickups to determine one-time pickup states that aren't reflected in inventory alone
4. **Cross-references flag IDs** captured live via [SoulSplitter](https://github.com/FrankvdStam/SoulSplitter)'s event flag logger while playing, mapping each one to a specific named location
5. **Serves the result** two ways: a headless watch loop that writes a JSON snapshot on every save change, or a local Flask dashboard with live-updating

No game files are modified. Everything is read-only

## Status

Gourd seeds are currently missing a few flag entries but will be finished extremely soon. Next up is testing and a need for input over what should be added or changed in the final product. A full dashboard is made and working with MY save file so that's where the testing comes in. Also figuring out the executable and download process for distrubution of the tool which will be added with screenshots here in the readme.

# Google Sheet for all triggered event flags for each prayer bead/gourd seed drop in the game: 

Prayer Bead: 
https://docs.google.com/spreadsheets/d/17YkjiKnKZTHUHFSkf_SZK5KQrgrUO5_V1XxE4lfPpLA/edit?gid=0#gid=0

Gourd Seed:
https://docs.google.com/spreadsheets/d/1BUwN0m1CTA2TQ7v4epO_x-rUQetOO8YpWVOXCfMXSrE/edit?gid=0#gid=0

## Credits

- Save file container structure adapted from [alfizari/Sekiro-Save-Editor](https://github.com/alfizari/Sekiro-Save-Editor)
- Event flag discovery informed by [SoulSplitter](https://github.com/FrankvdStam/SoulSplitter)'s wiki and live logger tooling
- Youtubers I used for the guides:
   - https://www.youtube.com/@Kenjidarou
   - https://www.youtube.com/@GuidesForUsAll
   - https://www.youtube.com/@Fextralife
   - https://www.youtube.com/@DarcbladeGuides
   - https://www.youtube.com/@GoldenOrder
