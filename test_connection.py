"""
test_connection.py

Run this ONCE, manually, to confirm the whole pipeline actually works
against your real save before trusting tracker.py's automatic loop.

    uv run test_connection.py

This does NOT modify anything -- pure read-only sanity check. Safe to
run with the game open or closed.
"""

from save_reader import default_save_path, read_save_file, extract_slot, find_active_slots
from stats_reader import read_stats
from achievements import build_report


def main():
    save_path = default_save_path()
    if save_path is None:
        print("Could not auto-locate S0000.sl2.")
        print("Expected under %APPDATA%\\Sekiro\\<SteamID>\\S0000.sl2")
        print("If it's somewhere else, hardcode the path below and rerun.")
        return

    print(f"Found save file: {save_path}\n")
    data = read_save_file(save_path)
    print(f"Read {len(data)} bytes total.\n")

    active = find_active_slots(data)
    print(f"Active-looking slots: {active}\n")

    if not active:
        print("No active slots detected -- something's off with the file "
              "or the 'active slot' heuristic needs adjusting.")
        return

    for slot_index in active:
        print(f"--- Slot {slot_index} ---")
        slot = extract_slot(data, slot_index)

        stats = read_stats(slot)
        print("Stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        report = build_report(slot)
        print("\nProsthetic tools owned:")
        for name, owned in report["prosthetic_tools"]["owned"].items():
            print(f"  {'YES' if owned else ' no'}  {name}")

        print("\nQuantity targets:")
        for name, info in report["quantity_targets"].items():
            print(f"  {name}: {info['have']} / {info['target']}")

        beads_mapped = sum(1 for v in report["prayer_beads"].values() if v is not None)
        print(f"\nPrayer beads mapped so far: {beads_mapped} "
              f"(rest show null -- expected, not an error)")
        print()


if __name__ == "__main__":
    main()
