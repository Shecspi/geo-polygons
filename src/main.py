import json

from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware


polygons_dir = Path().cwd()


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


@router_country.get("/all")
async def get_all_countries():
    """
    Возвращает полигоны всех стран мира.
    """
    path = Path(polygons_dir) / "country"
    files = path.glob("*.geojson")

    if not path.exists() or not any(path.iterdir()):
        return {"error": "Отсутствуют полигоны стран"}

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
    path = Path(polygons_dir) / f"country/{country_code}.geojson"

    if not path.exists():
        return {"error": f"Отсутствует полигон страны {country_code}"}

    with open(path, "r") as f:
        return json.loads(f.read())


@router_region.get("/{country_code}/all")
async def get_all_regions(country_code: str):
    """
    Возвращает полигоны всех регионов указанной страны.
    """
    path = Path(polygons_dir) / f"regions/{country_code}"
    files = path.glob("*.geojson")

    if not path.exists() or not any(path.iterdir()):
        return {"error": f"Отсутствуют полигоны регионов для страны {country_code}"}

    result = []
    for file in files:
        with open(file, "r") as f:
            polygon = json.loads(f.read())
        result.append(polygon)

    return result


@router_region.get("/{country_code}/{region_code}")
async def get_region(country_code: str, region_code: str):
    """
    Возвращает полигон указанного региона из указанной страны.
    """
    path = Path(polygons_dir) / f"regions/{country_code}/{region_code}.geojson"

    if not path.exists():
        return {
            "error": f"Отсутствует полигон для региона {region_code} в стране {country_code}"
        }

    with open(path, "r") as f:
        return json.loads(f.read())


# @router_region.get("/{country_code}/{area_code}/{region_code}")
# async def get_regions_in_area(country_code: str, area_code: str, region_code: str):
#     """
#     Возвращает полигоны всех регионов в указанном округе указанной страны.
#     Это может быть доступно не для всех стран, так как не у всех может быть деление на округа.
#     """


app.include_router(router_country, prefix="/country", tags=["country"])
app.include_router(router_region, prefix="/region", tags=["region"])
app.include_router(router_city, prefix="/city", tags=["city"])
