"""
scan_offset.py

Not written by me but ai as a tool to find the offset of the prayer bead table in Sekiro save files. 
It scans a full slot for known prayer bead flags and can also compare two snapshots to find where a specific flag flipped from 0 to 1.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from save_reader import read_save_file, extract_slot
from bead_map import PRAYER_BEADS

SNAP_DIR = Path("saves")


def _block_msb(f):
    # SoulSplitter SoulMemory/Sekiro/Sekiro.cs ReadEventFlag: blocks of 1000 flags;
    # read the u32 at ((id%1000)>>5)*4 and test bit 31 - (id%1000 & 31).
    m = f % 1000
    return (m // 32) * 4 + 3 - (m % 32) // 8, 7 - m % 8


def _flat_msb(f): return f // 8, 7 - f % 8
def _flat_lsb(f): return f // 8, f % 8
def _word_msb(f): return (f // 32) * 4 + 3 - (f % 32) // 8, 7 - f % 8
def _word_lsb(f): return (f // 32) * 4 + 3 - (f % 32) // 8, f % 8


LAYOUTS = {"sekiro-block": _block_msb, "msb": _flat_msb, "lsb": _flat_lsb,
           "msb-word": _word_msb, "lsb-word": _word_lsb}


def load_slot(label: str, slot: int) -> bytes:
    path = SNAP_DIR / f"{label}.sl2"
    if not path.exists():
        sys.exit(f"No snapshot at {path}. Run: uv run find_offset.py snap {label}")
    return extract_slot(read_save_file(path), slot)


def bit(data: bytes, off: int, pos: tuple[int, int]) -> bool:
    byte_i, shift = pos
    return bool((data[off + byte_i] >> shift) & 1)


def scan(full: bytes, flags: list[int], layout) -> list[int]:
    pos = [layout(f) for f in flags]
    span = max(p[0] for p in pos) + 1
    first, rest = pos[0], pos[1:]
    hits = []
    for off in range(0, len(full) - span):
        if not (full[off + first[0]] >> first[1]) & 1:
            continue
        if all((full[off + b] >> s) & 1 for b, s in rest):
            hits.append(off)
    return hits


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--full", nargs=2, metavar=("LABEL", "SLOT"), required=True)
    p.add_argument("--pair", nargs=4, metavar=("BEFORE", "AFTER", "SLOT", "FLAGID"))
    args = p.parse_args()

    flags = sorted({b.event_flag_id for b in PRAYER_BEADS if b.event_flag_id is not None})
    n = len(flags)
    print(f"Using {n} known bead flags: {flags[0]} .. {flags[-1]}")
    full = load_slot(args.full[0], int(args.full[1]))
    if args.pair:
        b_label, a_label, slot, fid = args.pair
        fid = int(fid)
        before, after = load_slot(b_label, int(slot)), load_slot(a_label, int(slot))

    found = False
    for name, layout in LAYOUTS.items():
        hits = scan(full, flags, layout)
        line = f"\n{name}: {len(hits)} offsets where all flags are set in the full slot"
        if not args.pair:
            print(line)
            for o in hits[:20]:
                found = True
                print(f"  0x{o:06X} ({o})")
            continue

        pos = {f: layout(f) for f in flags}
        rows = []
        for o in hits:
            if bit(before, o, pos[fid]) or not bit(after, o, pos[fid]):
                continue  # the picked-up flag must go 0 -> 1
            n_before = sum(bit(before, o, pos[f]) for f in flags)
            n_after = sum(bit(after, o, pos[f]) for f in flags)
            rows.append((n_after - n_before, n_before, o, n_after))
        rows.sort()  # best first: only 1 flag changed, then fewest set early
        print(line + f"; {len(rows)} where {fid} flipped 0 -> 1")
        for changed, n_before, o, n_after in rows:
            found = True
            tag = "   <-- only the pickup changed" if changed == 1 else ""
            print(f"  0x{o:06X} ({o})  early slot: {n_before}/{n} set -> after: {n_after}/{n}{tag}")
    if not found:
        print("\nNo candidates.")


if __name__ == "__main__":
    main()