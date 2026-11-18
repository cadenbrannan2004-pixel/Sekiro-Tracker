import json
import os
from pathlib import Path

# where web/ and the state JSON files live when running from source
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def save_json(path: Path, data) -> None:
    """Writes a temp file then renames it, so a reader never sees a half-written file."""
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)
