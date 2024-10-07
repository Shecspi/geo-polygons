import json
import time

import aiofiles
import redis
from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

polygons_dir = '/home/shecspi/Projects/geo-polygons'


app = FastAPI()
router_country = APIRouter()
router_region = APIRouter()
router_city = APIRouter()

r = redis.StrictRedis(
    host='localhost',
    port=6379,
    password='password'
)

origins = [
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    path = Path(f'/home/shecspi/Projects/geo-polygons/regions/RU')
    files = path.glob('*.geojson')
    result = []
    for file in files:
        with open(file, 'r') as f:
            result.append(json.load(f))

    return result


@router_country.get('/all')
async def get_all_countries():
    """
    Возвращает полигоны всех стран мира.
    """


@router_country.get('/{country_code}')
async def get_country(country_code: str):
    """
    Возвращает полигон переданной страны.
    """


@router_region.get('/{country_code}/all')
async def get_all_regions(country_code: str):
    """
    Возвращает полигоны всех регионов указанной страны.
    """
    p = Path(polygons_dir) / f'regions/{country_code}'
    files = p.glob('*.geojson')
    result = []

    start_time = time.perf_counter()
    for file in files:
        async with aiofiles.open(file, 'r') as f:
            a = await f.read()
    print(time.perf_counter() - start_time)

    return result


@router_region.get('/{country_code}/{region_code}')
async def get_region(country_code: str, region_code: str):
    """
    Возвращает полигон указанного региона из указанной страны.
    """


@router_region.get('/{country_code}/{area_code}/{region_code}')
async def get_regions_in_area(country_code: str, area_code: str, region_code: str):
    """
    Возвращает полигоны всех регионов в указанном округе указанной страны.
    Это может быть доступно не для всех стран, так как не у всех можеь быть деление на округа.
    """


@router_city.get('/{country_code}/all')
async def get_all_cities(country_code: str, region_code: str):
    """
    Возвращает geoJson-точки всех городов указанной страны.
    """


app.include_router(router_country, prefix='/country', tags=['country'])
app.include_router(router_region, prefix='/region', tags=['region'])
app.include_router(router_city, prefix='/city', tags=['city'])
