from fastapi import APIRouter, HTTPException
from src.services.country_service import get_all_countries, get_country

router = APIRouter()


@router.get("/all")
async def api_get_all_countries():
    try:
        return get_all_countries()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/hq/{country_code}")
async def api_get_country(country_code: str):
    try:
        return get_country(country_code)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
