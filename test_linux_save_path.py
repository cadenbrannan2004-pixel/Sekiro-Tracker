"""Builds fake Proton Steam trees under a temp HOME and checks default_save_path()
finds the save. Run with: python test_linux_save_path.py (any non-Windows OS)."""

import os
import tempfile
import time
from pathlib import Path

from save_reader import PROTON_SAVE_DIR, default_save_path
from steam_achievements import STEAM_ID64_BASE


def make_save(library: Path, steam_id: int) -> Path:
    save = library / PROTON_SAVE_DIR / str(steam_id) / "S0000.sl2"
    save.parent.mkdir(parents=True)
    save.write_bytes(b"\0")
    return save


def main():
    os.environ.pop("APPDATA", None)
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(os.path.realpath(tmp))
        os.environ["HOME"] = str(home)
        steam = home / ".local/share/Steam"

        assert default_save_path() is None, "no Steam install should mean no save"

        # Default library: picked when it's the only save
        older = make_save(steam, STEAM_ID64_BASE + 1)
        assert default_save_path() == older, default_save_path()

        # Extra library from libraryfolders.vdf with a newer save wins on mtime
        extra = home / "games/SteamLibrary"
        (steam / "steamapps/libraryfolders.vdf").write_text(
            f'"libraryfolders"\n{{\n\t"0"\n\t{{\n\t\t"path"\t\t"{steam}"\n\t}}\n'
            f'\t"1"\n\t{{\n\t\t"path"\t\t"{extra}"\n\t}}\n}}\n')
        time.sleep(0.01)
        newer = make_save(extra, STEAM_ID64_BASE + 2)
        assert default_save_path() == newer, default_save_path()

        # Active Steam account from registry.vdf beats the newest save
        (home / ".steam").mkdir()
        (home / ".steam/registry.vdf").write_text(
            '"Registry"\n{\n\t"HKCU"\n\t{\n\t\t"Software"\n\t\t{\n\t\t\t"Valve"\n\t\t\t{\n'
            '\t\t\t\t"Steam"\n\t\t\t\t{\n\t\t\t\t\t"ActiveProcess"\n\t\t\t\t\t{\n'
            '\t\t\t\t\t\t"pid"\t\t"1234"\n\t\t\t\t\t\t"ActiveUser"\t\t"1"\n'
            '\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n')
        assert default_save_path() == older, default_save_path()

        # ActiveUser 0 (signed out) falls back to the newest save
        reg = home / ".steam/registry.vdf"
        reg.write_text(reg.read_text().replace('"ActiveUser"\t\t"1"', '"ActiveUser"\t\t"0"'))
        assert default_save_path() == newer, default_save_path()

    print("OK: Linux save detection")


if __name__ == "__main__":
    main()
