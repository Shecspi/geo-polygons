from fastapi import APIRouter, HTTPException
from src.services.region_service import get_all_regions, get_region

router = APIRouter()


@router.get("/lq/{country_code}/all")
async def api_get_all_regions(country_code: str):
    try:
        return get_all_regions(country_code)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/lq/{country_code}/{region_code}")
async def api_get_region_lq(country_code: str, region_code: str):
    try:
        return get_region(country_code, region_code, quality="LQ")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/hq/{country_code}/{region_code}")
async def api_get_region_hq(country_code: str, region_code: str):
    try:
        return get_region(country_code, region_code, quality="HQ")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
