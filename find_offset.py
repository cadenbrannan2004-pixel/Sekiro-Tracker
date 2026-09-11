"""
find_offset.py

Helper for discovering event_flags.FLAG_TABLE_OFFSET empirically.

The idea: pick up ONE bead between two save snapshots, diff them, and find
the single bit that flipped 0 -> 1. Given the bead's event_flag_id, that
bit's byte position tells you where the flag table starts.

CLEAN CAPTURE (this matters -- a noisy capture is useless):

  1. Fight your way to the bead/chest. Kill every enemy nearby. Stand
     right next to it -- do NOT open it yet.
  2. Quit to the MAIN MENU (this writes S0000.sl2 and, on reload, puts you
     back exactly here with the enemies still dead).
         uv run find_offset.py snap before
  3. Load back in. Open the chest / grab the bead. Do NOTHING else -- no
     fighting, no running around, no resting at an idol.
  4. Quit to the main menu immediately.
         uv run find_offset.py snap after
  5. uv run find_offset.py diff before after --flag-id <id> --slot <n>

     (event_flag_id values are in bead_map.py: attic chest = 6788,
      castle map-room hidden wall = 6790, Blazing Bull = 6711, ...)

If one clean pair still looks ambiguous, do a second bead the same way
with different labels and intersect:

  uv run find_offset.py intersect --slot 2 \
      --pair before after 6790 \
      --pair before2 after2 6711

The offset that survives the intersection is the answer. Hardcode it in
event_flags.py as FLAG_TABLE_OFFSET.

Snapshots live in ./saves/ (already gitignored).
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from save_reader import default_save_path, read_save_file, extract_slot

SNAP_DIR = Path("saves")


def cmd_snap(args: argparse.Namespace) -> None:
    src = default_save_path()
    if src is None:
        sys.exit("Could not locate S0000.sl2 -- has the game saved at least once?")
    SNAP_DIR.mkdir(exist_ok=True)
    dst = SNAP_DIR / f"{args.label}.sl2"
    shutil.copy2(src, dst)
    print(f"Copied {src}")
    print(f"     -> {dst}  ({dst.stat().st_size} bytes)")
    print("Make sure you quit to the main menu before this snap so the copy is current.")


def _load_slot(label: str, slot_index: int) -> bytes:
    path = SNAP_DIR / f"{label}.sl2"
    if not path.exists():
        sys.exit(f"No snapshot at {path}.  Run:  uv run find_offset.py snap {label}")
    return extract_slot(read_save_file(path), slot_index)


def _zero_to_one_flips(before: bytes, after: bytes) -> list[tuple[int, int]]:
    """(byte_offset, bit_pos) for every bit that went 0 -> 1.

    bit_pos is MSB-first (0 = 0x80 ... 7 = 0x01), matching event_flags.read_flag.
    """
    out = []
    for off, (b, a) in enumerate(zip(before, after)):
        newly_set = a & ~b  # bits that are 1 in 'after' but were 0 in 'before'
        if not newly_set:
            continue
        for bit in range(8):
            if newly_set & (1 << (7 - bit)):
                out.append((off, bit))
    return out


def _implied_offsets(before: bytes, after: bytes, flag_id: int) -> dict[str, set[int]]:
    """For each bit-ordering convention, the set of FLAG_TABLE_OFFSET values
    that would make some observed 0->1 flip == this flag_id."""
    byte_in_table = flag_id // 8
    want_msb = 7 - (flag_id % 8)
    want_lsb = flag_id % 8
    msb, lsb = set(), set()
    for off, bit in _zero_to_one_flips(before, after):
        if bit == want_msb:
            msb.add(off - byte_in_table)
        if bit == want_lsb:
            lsb.add(off - byte_in_table)
    return {"MSB-first": msb, "LSB-first": lsb}


def cmd_diff(args: argparse.Namespace) -> None:
    before = _load_slot(args.before, args.slot)
    after = _load_slot(args.after, args.slot)
    if len(before) != len(after):
        sys.exit("Snapshots differ in slot size -- wrong slot or corrupt copy.")

    changed_bytes = sum(1 for b, a in zip(before, after) if b != a)
    flips = _zero_to_one_flips(before, after)
    print(f"Slot {args.slot}: {changed_bytes} bytes differ, {len(flips)} bits went 0 -> 1 "
          f"between '{args.before}' and '{args.after}'.")
    if changed_bytes > 300:
        print("  ! Very noisy. Something other than the single pickup changed "
              "(fighting, movement, idol rest). A clean capture is usually < 100 bytes.")

    if args.flag_id is None:
        print("\nPass --flag-id <event_flag_id from bead_map.py> to locate the table.")
        for off, bit in flips[:60]:
            print(f"  byte 0x{off:06X} ({off})  bit {bit}")
        return

    cand = _implied_offsets(before, after, args.flag_id)
    print(f"\nFor flag_id {args.flag_id}, candidate FLAG_TABLE_OFFSET values:")
    for ordering, offsets in cand.items():
        if not offsets:
            print(f"  {ordering}: (no 0->1 flip at the expected bit position)")
            continue
        for o in sorted(offsets):
            print(f"  {ordering}: 0x{o:06X} ({o})")
    print("\nIf there are still several candidates, run a second bead and "
          "`intersect` -- see the header of this file.")


def cmd_intersect(args: argparse.Namespace) -> None:
    if not args.pair or len(args.pair) < 2:
        sys.exit("Need at least two --pair BEFORE AFTER FLAGID arguments.")

    per_ordering: dict[str, list[set[int]]] = {"MSB-first": [], "LSB-first": []}
    for before_label, after_label, flag_id_str in args.pair:
        flag_id = int(flag_id_str)
        before = _load_slot(before_label, args.slot)
        after = _load_slot(after_label, args.slot)
        changed = sum(1 for b, a in zip(before, after) if b != a)
        cand = _implied_offsets(before, after, flag_id)
        print(f"pair ({before_label} -> {after_label}, flag {flag_id}): "
              f"{changed} bytes changed; "
              f"MSB candidates={len(cand['MSB-first'])}, LSB candidates={len(cand['LSB-first'])}")
        per_ordering["MSB-first"].append(cand["MSB-first"])
        per_ordering["LSB-first"].append(cand["LSB-first"])

    print("\nOffsets consistent across ALL pairs:")
    hit = False
    for ordering, sets in per_ordering.items():
        common = set.intersection(*sets) if sets else set()
        for o in sorted(common):
            hit = True
            print(f"  {ordering}:  FLAG_TABLE_OFFSET = 0x{o:06X} ({o})")
    if not hit:
        print("  (none -- captures are too noisy, or the slot index is wrong, "
              "or the two beads' flags weren't actually freshly set)")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("snap", help="copy the live save to ./saves/<label>.sl2")
    s.add_argument("label", help="e.g. before / after / before2 ...")
    s.set_defaults(func=cmd_snap)

    d = sub.add_parser("diff", help="diff two snapshots and locate the flag table")
    d.add_argument("before")
    d.add_argument("after")
    d.add_argument("--slot", type=int, default=0)
    d.add_argument("--flag-id", type=int, default=None,
                   help="event_flag_id you expect to have flipped (see bead_map.py)")
    d.set_defaults(func=cmd_diff)

    i = sub.add_parser("intersect", help="find the offset consistent across several pairs")
    i.add_argument("--slot", type=int, default=0)
    i.add_argument("--pair", action="append", nargs=3, metavar=("BEFORE", "AFTER", "FLAGID"),
                   help="a before label, an after label, and the expected event_flag_id")
    i.set_defaults(func=cmd_intersect)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
