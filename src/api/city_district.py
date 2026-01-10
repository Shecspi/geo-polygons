from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.city_district_service import get_city_districts

router = APIRouter()


class CityDistrictRequest(BaseModel):
    country_code: str
    region_code: str
    city_name: str


@router.post("/lq")
async def api_get_city_districts_lq(request: CityDistrictRequest):
    """
    Возвращает все полигоны районов города (низкое качество).

    Принимает в теле запроса:
    - country_code: код страны
    - region_code: код региона
    - city_name: название города

    Возвращает список всех GeoJSON файлов из папки polygons/LQ/city_districts/{country_code}/{region_code}/{city_name}
    """
    try:
        return get_city_districts(
            request.country_code, request.region_code, request.city_name, quality="LQ"
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/hq")
async def api_get_city_districts_hq(request: CityDistrictRequest):
    """
    Возвращает все полигоны районов города (высокое качество).

    Принимает в теле запроса:
    - country_code: код страны
    - region_code: код региона
    - city_name: название города

    Возвращает список всех GeoJSON файлов из папки polygons/HQ/city_districts/{country_code}/{region_code}/{city_name}
    """
    try:
        return get_city_districts(
            request.country_code, request.region_code, request.city_name, quality="HQ"
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
