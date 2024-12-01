import json
import logging
import os

from pathlib import Path
from typing import Literal

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


type RunType = Literal["local", "docker"]


class Settings(BaseSettings):
    # Тип запуска приложения - локально или через Docker
    RUN_TYPE: RunType


class LocalSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.local")

    # Корневая директория приложения
    BASE_DIR: str = str(Path().cwd())


class DockerSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.prod")

    # Корневая директория приложения
    BASE_DIR: str = str(Path().cwd().parent)


# os.getenv("RUN_TYPE") объявлена только в docker0compose файле.
# Если она есть, значит запуск происодит через Docker. Иначе - локальный запуск.
if os.getenv("RUN_TYPE") == "docker":
    settings = DockerSettings()
else:
    settings = LocalSettings()


logging.basicConfig(
    level=logging.INFO,
    filename="log.log",
    filemode="w+",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


app = FastAPI()
router_country = APIRouter()
router_region = APIRouter()
router_city = APIRouter()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AllRegionsOfCountryModel(BaseModel): ...


@router_country.get("/all")
async def get_all_countries():
    """
    Возвращает полигоны всех стран мира.
    """
    path = Path(settings.BASE_DIR) / "polygons/LQ/countries"
    files = path.glob("*.geojson")

    if not path.exists() or not any(path.iterdir()):
        raise HTTPException(
            status_code=404,
            detail="Отсутствуют полигоны стран",
        )

    result = []
    for file in files:
        with open(file, "r") as f:
            polygon = json.loads(f.read())
        result.append(polygon)

    return result


@router_country.get("/{country_code}")
async def get_country(country_code: str):
    """
    Возвращает полигон переданной страны.
    """
    path = Path(settings.BASE_DIR) / f"country/{country_code}.geojson"

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Отсутствует полигон страны {country_code}",
        )

    with open(path, "r") as f:
        return json.loads(f.read())


@router_region.get("/lq/{country_code}/all")
async def get_all_regions(country_code: str):
    """
    Возвращает полигоны всех регионов указанной страны.
    """
    path = Path(settings.BASE_DIR) / f"polygons/LQ/regions/{country_code}"
    files = path.glob("*.geojson")

    if not path.exists() or not any(path.iterdir()):
        logging.warning("Отсутствуют полигоны регионов для страны %s", country_code)
        raise HTTPException(
            status_code=404,
            detail=f"Отсутствуют полигоны регионов для страны {country_code}",
        )

    result = []
    for file in files:
        with open(file, "r") as f:
            polygon = json.loads(f.read())
        result.append(polygon)

    logging.info("Загружены полигоны всех регионов для страны %s", country_code)

    return result


@router_region.get("/lq/{country_code}/{region_code}")
async def get_region(country_code: str, region_code: str):
    """
    Возвращает полигон указанного региона из указанной страны.
    """
    path = (
        Path(settings.BASE_DIR)
        / f"polygons/LQ/regions/{country_code}/{region_code}.geojson"
    )

    if not path.exists():
        logging.warning(
            "Отсутствует полигон региона %s в стране %s",
            region_code,
            country_code,
        )
        raise HTTPException(
            status_code=404,
            detail=f"Отсутствует полигон для региона {region_code} в стране {country_code}",
        )

    with open(path, "r") as f:
        logging.info(
            "Загружен полигон для региона %s в стране %s", region_code, country_code
        )
        return json.loads(f.read())


@router_region.get("/hq/{country_code}/{region_code}")
async def get_hq_region(country_code: str, region_code: str):
    """
    Возвращает полигон указанного региона из указанной страны.
    """
    path = (
        Path(settings.BASE_DIR)
        / f"polygons/HQ/regions/{country_code}/{region_code}.geojson"
    )

    if not path.exists():
        logging.warning(
            "Отсутствует полигон региона %s в стране %s",
            region_code,
            country_code,
        )
        raise HTTPException(
            status_code=404,
            detail=f"Отсутствует полигон для региона {region_code} в стране {country_code}",
        )

    with open(path, "r") as f:
        logging.info(
            "Загружен полигон для региона %s в стране %s", region_code, country_code
        )
        return json.loads(f.read())


app.include_router(router_country, prefix="/country", tags=["country"])
app.include_router(router_region, prefix="/region", tags=["region"])
app.include_router(router_city, prefix="/city", tags=["city"])
