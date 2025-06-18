from pathlib import Path
from typing import List

from src.infrastructure.file_loader import load_geojson_file, load_all_geojson_files
from src.core.config import settings


def get_all_regions(country_code: str) -> List[dict]:
    path = Path(settings.BASE_DIR) / f"polygons/LQ/regions/{country_code}"
    polygons = load_all_geojson_files(path)
    if not polygons:
        raise FileNotFoundError(
            f"Полигоны регионов для страны {country_code} не найдены"
        )
    return polygons


def get_region(country_code: str, region_code: str, quality: str = "LQ") -> dict:
    path = (
        Path(settings.BASE_DIR)
        / f"polygons/{quality}/regions/{country_code}/{region_code}.geojson"
    )
    polygon = load_geojson_file(path)
    if polygon is None:
        raise FileNotFoundError(
            f"Регион {region_code} в стране {country_code} не найден"
        )
    return polygon
