# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Sekiro: Shadows Die Twice players going for 100% completion. They keep the dashboard open while playing (second monitor, often a dark room) or check it between sessions (laptop, daylight). Both scenes are real, so the user picks light or dark.

## Product Purpose
Reads the Sekiro PC save file (`S0000.sl2`) directly and shows, live, which prayer beads, gourd seeds, prosthetic tools and material targets a save slot has, plus a manual endings checklist. The game has no completion tracker, and stackable items like prayer beads can't tell you *which* locations are done. Success: the player knows what's left and where, without opening a wiki.

## Positioning
It reads the real save file and updates itself as you play, so nothing is entered by hand except the endings.

## Operating Context
- Runs locally: `SekiroApp.py` (or `tracker.py` + `server.py`) serves `web/` on 127.0.0.1 and polls `/api/state` every 3 s.
- Up to 10 save slots, each with an NG+ level.
- Some event flags aren't mapped yet; those items show as "flag not mapped" (null), not as missing.
- Bead rows and tools can link to a YouTube guide; endings can link to an ending guide.
- Endings are ticked manually and stored in `ending_state.json`.

## Capabilities and Constraints
- Read-only: it never writes to the save file.
- Plain static HTML/CSS/JS in `web/`, with no build step. It's bundled into a PyInstaller exe, so the page must work offline apart from optional web fonts.
- Optional `web/banner.png`: if it exists, it shows in the header (user wants to keep this).
- Fan-made; not affiliated with FromSoftware or Activision.

## Brand Commitments
- Name: "Sekiro Tracker".
- Visual theme pinned by the user (2026-10-20): sakura tree theme, with a few slowly drifting petals and a light/dark choice for the user.
- Look chosen by the user (2026-10-20): the standard tracker-dashboard layout, kept simple, with sakura colours. The user can drop their own `web/banner.png` and a `web/background.gif` of flowing petals into the page.

## Evidence on Hand
Real game data comes from the save via the API. No screenshots, testimonials or usage stats exist; don't invent any.

## Product Principles
- The save is the truth: show what the save says, and say clearly when something is unknown.
- What's left matters more than what's done.
- Check it at a glance, mid-session.
- Never touch the player's files.
