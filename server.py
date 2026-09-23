"""
server.py

Local web frontend for the Sekiro tracker.

Serves achievement_state.json (written on a loop by tracker.py) as JSON
over HTTP, and persists a manual ending checklist to ending_state.json.

Run alongside tracker.py:
    uv run tracker.py       # in one terminal
    uv run server.py        # in another
Then open http://127.0.0.1:5000
"""

import json
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from endings import ENDINGS

APP_ROOT = Path(__file__).parent
STATE_PATH = APP_ROOT / "achievement_state.json"
ENDING_STATE_PATH = APP_ROOT / "ending_state.json"
WEB_DIR = APP_ROOT / "web"

app = Flask(__name__, static_folder=None)


def _load_json(path: Path, default):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


@app.route("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(WEB_DIR, filename)


@app.route("/api/state")
def api_state():
    state = _load_json(STATE_PATH, None)
    if state is None:
        return jsonify({"error": "achievement_state.json not found yet -- "
                                  "is tracker.py running?"}), 404
    return jsonify(state)


@app.route("/api/endings", methods=["GET"])
def api_endings_get():
    checked = _load_json(ENDING_STATE_PATH, {})
    return jsonify({
        "endings": [
            {
                "id": ending.id,
                "name": ending.name,
                "requirements": [
                    {"id": req.id, "text": req.text, "checked": checked.get(req.id, False)}
                    for req in ending.requirements
                ],
            }
            for ending in ENDINGS
        ]
    })


@app.route("/api/endings", methods=["POST"])
def api_endings_post():
    payload = request.get_json(force=True, silent=True) or {}
    req_id = payload.get("id")
    checked_value = payload.get("checked")

    valid_ids = {req.id for ending in ENDINGS for req in ending.requirements}
    if req_id not in valid_ids or not isinstance(checked_value, bool):
        return jsonify({"error": "expected {id: <known requirement id>, checked: <bool>}"}), 400

    state = _load_json(ENDING_STATE_PATH, {})
    state[req_id] = checked_value
    with open(ENDING_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
