import json
from pathlib import Path


def load_geojson_file(path: Path) -> dict | None:
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)


def load_all_geojson_files(folder: Path) -> list[dict]:
    if not folder.exists() or not any(folder.iterdir()):
        return []
    return [json.load(open(file)) for file in folder.glob("*.geojson")]
