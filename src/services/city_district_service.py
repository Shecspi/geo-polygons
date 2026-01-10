from pathlib import Path

from src.infrastructure.file_loader import load_all_geojson_files
from src.core.config import settings


def get_city_districts(
    country_code: str, region_code: str, city_name: str, quality: str = "LQ"
) -> list[dict]:
    """
    Возвращает все полигоны районов города из папки.

    Args:
        country_code: Код страны
        region_code: Код региона
        city_name: Название города
        quality: Качество полигонов (HQ или LQ)

    Returns:
        Список GeoJSON объектов с полигонами районов города

    Raises:
        FileNotFoundError: Если папка не найдена или пуста
    """
    # polygons/HQ/city_districts/RU/MOW
    path = (
        Path(settings.BASE_DIR)
        / f"polygons/{quality.upper()}/city_districts/{country_code}/{region_code}/{city_name}"
    )
    polygons = load_all_geojson_files(path)
    if not polygons:
        raise FileNotFoundError(
            f"Полигоны районов города {city_name} в регионе {region_code} страны {country_code} не найдены"
        )
    return polygons
