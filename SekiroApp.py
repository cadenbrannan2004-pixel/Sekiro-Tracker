"""
SekiroApp.py

Runs the save watcher (tracker.py) and the web dashboard (server.py) in one process, then opens the dashboard.

"""

import sys
import threading
import webbrowser
from pathlib import Path

from werkzeug.serving import make_server

import server
import tracker

# A --onefile exe unpacks bundled files to a temp dir (sys._MEIPASS) that is
# wiped on exit, so web files load from there but JSON state lives beside the exe.
if getattr(sys, "frozen", False):
    data_dir = Path(sys.executable).parent
    server.WEB_DIR = Path(sys._MEIPASS) / "web"
    server.STATE_PATH = tracker.OUTPUT_PATH = data_dir / "achievement_state.json"
    server.ENDING_STATE_PATH = data_dir / "ending_state.json"


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
    print(f"Dashboard: {url}  (Ctrl+C to quit)")
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
