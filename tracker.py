"""
tracker.py

Automatic loop: watches the save file for changes, re-parses the active
slot, and writes out current prayer bead pickup state as JSON. Run this
alongside the game.
"""

import json
import time
from pathlib import Path

from save_reader import default_save_path, read_save_file, extract_slot, find_active_slots
from achievements import build_report

OUTPUT_PATH = Path("achievement_state.json")
POLL_INTERVAL_SECONDS = 3
SLOT_INDEX = 0  # adjust if you track a non-default character slot


def run():
    save_path = default_save_path()
    if save_path is None:
        raise SystemExit(
            "Could not auto-locate S0000.sl2. Set the path manually in "
            "save_reader.default_save_path() or pass it in directly."
        )

    print(f"Watching: {save_path}")
    last_mtime = None

    while True:
        try:
            mtime = save_path.stat().st_mtime
        except FileNotFoundError:
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        if mtime != last_mtime:
            last_mtime = mtime
            data = read_save_file(save_path)
            slot = extract_slot(data, SLOT_INDEX)
            report = build_report(slot)

            with open(OUTPUT_PATH, "w") as f:
                json.dump(report, f, indent=2)

            beads_done = sum(1 for v in report["prayer_beads"].values() if v)
            tools_missing = len(report["prosthetic_tools"]["missing"])
            print(
                f"Save changed -> beads: {beads_done}, "
                f"prosthetics missing: {tools_missing}"
            )

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
