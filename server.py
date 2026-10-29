
import json
from pathlib import Path

from flask import Flask, Response, jsonify, request, send_from_directory

import app_settings
from boss_map import MANUAL_IDS, get_account_bosses
from endings import ENDINGS
from save_reader import default_save_path, save_owner_steam_id64
from steam_achievements import read_achievements

APP_ROOT = Path(__file__).parent
STATE_PATH = APP_ROOT / "achievement_state.json"
ENDING_STATE_PATH = APP_ROOT / "ending_state.json"
BOSS_STATE_PATH = APP_ROOT / "boss_state.json"
SLOT_NAMES_PATH = APP_ROOT / "slot_names.json"
WEB_DIR = APP_ROOT / "web"
MAX_NAME_LENGTH = 32

app = Flask(__name__, static_folder=None)


def _load_json(path: Path, default):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


def _save_json(path: Path, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def index():
    # Settings go on the <html> tag so the saved theme applies before first paint.
    # They live in a file, not localStorage, because the exe gets a new port (origin) every launch.
    attrs = app_settings.html_attrs(app_settings.load())
    page = (WEB_DIR / "index.html").read_text(encoding="utf-8")
    page = page.replace('<html lang="en">', f'<html lang="en"{attrs}>', 1)
    return Response(page, mimetype="text/html")


# Only the save file location, since everything else is already on the <html> tag
@app.route("/api/settings", methods=["GET"])
def api_settings_get():
    detected = default_save_path()
    return jsonify({
        "savePath": app_settings.load().get("savePath", ""),
        "detectedSavePath": str(detected) if detected else "",
    })


@app.route("/api/settings", methods=["POST"])
def api_settings_post():
    payload = request.get_json(force=True, silent=True) or {}
    error = app_settings.update(payload)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"ok": True})


@app.route("/api/settings/reset", methods=["POST"])
def api_settings_reset():
    app_settings.reset()
    return jsonify({"ok": True})


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(WEB_DIR, filename)


def _current_account() -> str | None:
    """steamid64 (as a string) of the account whose save is being tracked."""
    save_path = app_settings.save_path()
    steam_id = save_owner_steam_id64(save_path) if save_path else None
    return None if steam_id is None else str(steam_id)


@app.route("/api/state")
def api_state():
    state = _load_json(STATE_PATH, None)
    if state is None:
        return jsonify({"error": "achievement_state.json not found yet -- "
                                  "is tracker.py running?"}), 404

    # A name belongs to the character in that slot, so drop it once the save is deleted
    names = _load_json(SLOT_NAMES_PATH, {})
    kept = {slot: name for slot, name in names.items() if slot in state.get("slots", {})}
    if kept != names:
        _save_json(SLOT_NAMES_PATH, kept)
    state["names"] = kept
    account = _current_account()
    achievements = read_achievements(int(account)) if account else None
    checked = _load_json(BOSS_STATE_PATH, {}).get(account, {}) if account else {}
    state["bosses"] = get_account_bosses(achievements, checked)
    return jsonify(state)


@app.route("/api/slot-names", methods=["POST"])
def api_slot_names_post():
    payload = request.get_json(force=True, silent=True) or {}
    slot = payload.get("slot")
    name = payload.get("name")

    state = _load_json(STATE_PATH, {}) or {}
    if slot not in state.get("slots", {}) or not isinstance(name, str):
        return jsonify({"error": "expected {slot: <active slot id>, name: <string>}"}), 400

    names = _load_json(SLOT_NAMES_PATH, {})
    name = name.strip()[:MAX_NAME_LENGTH]
    if name:
        names[slot] = name
    else:
        names.pop(slot, None)  # blank = back to the default "Slot N"
    _save_json(SLOT_NAMES_PATH, names)
    return jsonify({"ok": True, "name": name})


@app.route("/api/endings", methods=["GET"])
def api_endings_get():
    checked = _load_json(ENDING_STATE_PATH, {})
    return jsonify({
        "endings": [
            {
                "id": ending.id,
                "name": ending.name,
                "video": ending.video,
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
    _save_json(ENDING_STATE_PATH, state)
    return jsonify({"ok": True})



# Manual checks for bosses Steam has no achievement for, kept per Steam account
@app.route("/api/bosses", methods=["POST"])
def api_bosses_post():
    payload = request.get_json(force=True, silent=True) or {}
    boss_id = payload.get("id")
    checked_value = payload.get("checked")
    if boss_id not in MANUAL_IDS or not isinstance(checked_value, bool):
        return jsonify({"error": "expected {id: <manual boss id>, checked: <bool>}"}), 400

    account = _current_account()
    if account is None:
        return jsonify({"error": "no Steam account save found"}), 409
    state = _load_json(BOSS_STATE_PATH, {})
    state.setdefault(account, {})[boss_id] = checked_value
    _save_json(BOSS_STATE_PATH, state)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
