from pathlib import Path

from src.infrastructure.file_loader import load_geojson_file, load_all_geojson_files
from src.core.config import settings


def get_all_countries() -> list[dict]:
    path = Path(settings.BASE_DIR) / "polygons/LQ/countries"
    polygons = load_all_geojson_files(path)
    if not polygons:
        raise FileNotFoundError("Отсутствуют полигоны стран")
    return polygons


def get_country(country_code: str) -> dict:
    path = Path(settings.BASE_DIR) / f"polygons/HQ/countries/{country_code}.geojson"
    polygon = load_geojson_file(path)
    if polygon is None:
        raise FileNotFoundError(f"Страна {country_code} не найдена")
    return polygon
