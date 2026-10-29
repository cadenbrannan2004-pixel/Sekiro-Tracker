"""
SekiroApp.py

Runs the save watcher (tracker.py) and the web dashboard (server.py) in one process, then opens the dashboard.

"""

import sys
import threading
import time
import webbrowser
from pathlib import Path

from werkzeug.serving import make_server

import app_settings
import server
import tracker

# A --onefile exe unpacks bundled files to a temp dir (sys._MEIPASS) that is
# wiped on exit, so web files load from there but JSON state lives beside the exe.
if getattr(sys, "frozen", False):
    data_dir = Path(sys.executable).parent
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


# Closing the tab sends /api/bye. A reload sends it too, so wait a few seconds
# for the page to come back before shutting down. The "Close the app when the
# tab closes" setting turns this off, leaving the console window to quit with.
BYE_GRACE_SECONDS = 5
last_request = time.monotonic()
said_bye = False


@server.app.before_request
def note_request():
    global last_request, said_bye
    last_request = time.monotonic()
    said_bye = False


@server.app.post("/api/bye")
def bye():
    global said_bye
    said_bye = True
    return "", 204


def close_when_tab_closes(httpd):
    while not (said_bye and time.monotonic() - last_request > BYE_GRACE_SECONDS
               and app_settings.load().get("autoClose") != "off"):
        time.sleep(1)
    print("Dashboard tab closed, shutting down.")
    httpd.shutdown()


def main():
    threading.Thread(target=watch, daemon=True).start()

    # Port 0 = the OS assigns a free ephemeral port
    httpd = make_server("127.0.0.1", 0, server.app, threaded=True)
    url = f"http://127.0.0.1:{httpd.server_port}"
    print(f"Dashboard: {url}  (Ctrl+C to quit)")
    webbrowser.open(url)
    threading.Thread(target=close_when_tab_closes, args=(httpd,), daemon=True).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
