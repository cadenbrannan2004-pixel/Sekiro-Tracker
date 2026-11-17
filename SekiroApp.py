
import os
import shutil
import sys
import threading
from pathlib import Path

import webview
from werkzeug.serving import make_server

import app_settings
import server
import tracker

DATA_FILES = ("achievement_state.json", "ending_state.json", "boss_state.json",
              "slot_names.json", "settings.json")


def user_data_dir() -> Path:
    """%APPDATA%\\SekiroTracker on Windows, $XDG_DATA_HOME/SekiroTracker on Linux,
    so the exe can live anywhere without scattering JSON files."""
    # Older versions saved beside the exe (or in ~/SekiroTracker on Linux); move those over once
    old_dirs = [Path(sys.executable).parent]
    if sys.platform == "win32":
        data_dir = Path(os.environ.get("APPDATA") or Path.home()) / "SekiroTracker"
    else:
        data_dir = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share") / "SekiroTracker"
        old_dirs.append(Path.home() / "SekiroTracker")
    data_dir.mkdir(parents=True, exist_ok=True)
    for old_dir in old_dirs:
        for name in DATA_FILES:
            old, new = old_dir / name, data_dir / name
            if old.exists() and not new.exists():
                shutil.move(old, new)
    return data_dir


# A --onefile exe unpacks bundled files to a temp dir (sys._MEIPASS) that is
# wiped on exit, so web files load from there but JSON state lives in AppData.
if getattr(sys, "frozen", False):
    data_dir = user_data_dir()
    server.WEB_DIR = Path(sys._MEIPASS) / "web"
    server.STATE_PATH = tracker.OUTPUT_PATH = data_dir / "achievement_state.json"
    server.ENDING_STATE_PATH = data_dir / "ending_state.json"
    server.BOSS_STATE_PATH = data_dir / "boss_state.json"
    server.SLOT_NAMES_PATH = data_dir / "slot_names.json"
    app_settings.SETTINGS_PATH = data_dir / "settings.json"


def watch():
    # SystemExit inside a thread is swallowed silently, so surface its message
    try:
        tracker.run()
    except SystemExit as exc:
        print(exc)


def main():
    threading.Thread(target=watch, daemon=True).start()

    # Port 0 = the OS assigns a free ephemeral port
    httpd = make_server("127.0.0.1", 0, server.app, threaded=True)
    url = f"http://127.0.0.1:{httpd.server_port}"
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    # start() blocks until the window is closed, which quits the app.
    webview.create_window("Sekiro Tracker", url, width=1280, height=860, min_size=(480, 400))
    # Windows takes the .ico; GTK/Qt want a PNG, and no icon beats a broken one
    icon = server.WEB_DIR / ("DeathKanji.ico" if sys.platform == "win32" else "DeathKanji.png")
    webview.start(**({"icon": str(icon)} if icon.exists() else {}))
    httpd.shutdown()


if __name__ == "__main__":
    main()
