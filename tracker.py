"""
tracker.py

Automatic loop: watches the save file for changes, re-parses the active
slot, and writes each slot to a tracked state on one JSON file. This needs to 
run in the background while you play.
"""

import json
import os
import time
from pathlib import Path

import app_settings
from save_reader import read_save_file, extract_slot, find_active_slots
from achievements import build_report
from stats_reader import read_stats

# Anchored to this file's folder so server.py finds it no matter where tracker.py is launched from
OUTPUT_PATH = Path(__file__).parent / "achievement_state.json"



def run():
    save_path = None
    last_mtime = None

    while True:
        # Re-read every pass so a save location or refresh rate changed in Settings applies right away
        interval = app_settings.refresh_seconds()
        current = app_settings.save_path()
        if current != save_path:
            save_path, last_mtime = current, None
            print(f"Watching: {save_path}" if save_path else
                  "Could not auto-locate S0000.sl2. Set its location in the dashboard's Settings tab.")
        if save_path is None:
            time.sleep(interval)
            continue

        try:
            mtime = save_path.stat().st_mtime
        except FileNotFoundError:
            time.sleep(interval)
            continue

        if mtime != last_mtime:
            last_mtime = mtime
            try:
                data = read_save_file(save_path)
                active = find_active_slots(data)
            except Exception as exc:  # e.g. a file picked in Settings that isn't a Sekiro save
                print(f"Could not read {save_path}: {exc}")
                time.sleep(interval)
                continue
            slots = {}
            for idx in active:
                slot = extract_slot(data, idx)
                try:
                    report = build_report(slot)
                except Exception as exc: # a bad slot read will not effect the others
                    print(f"Slot {idx}: failed to build report: {exc}")
                    continue
                slots[str(idx)] = {"stats": read_stats(slot), "report": report}

            # this will create a temporary file first, then rename it to the final name. This avoids
            # a race condition where the web app reads the file while it's being written and gets a half file
            tmp = OUTPUT_PATH.with_suffix(".tmp")
            with open(tmp, "w") as f:
                json.dump({"updated": time.time(), "save_file": save_path.name, "slots": slots}, f, indent=2)
            os.replace(tmp, OUTPUT_PATH)

            for idx, slot in slots.items():
                r = slot["report"]
                beads = sum(1 for b in r["prayer_beads"] if b["collected"])
                targets = r["quantity_targets"]
                complete = sum(1 for t in targets.values() if t["complete"])
                print(f"Slot {idx}: {beads} prayer beads collected, "
                      f"{complete} / {len(targets)} quantity targets complete")

        # Sleep every pass, not just when the save changed, so the loop doesn't spin at 100% CPU
        time.sleep(interval)


if __name__ == "__main__":
    run()
        