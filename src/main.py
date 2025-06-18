from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import country, region

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(country.router, prefix="/country", tags=["country"])
app.include_router(region.router, prefix="/region", tags=["region"])
