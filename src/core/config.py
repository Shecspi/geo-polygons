import os

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


RunType = Literal["local", "docker"]


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
    BASE_DIR: str = str(Path().cwd())


# os.getenv("RUN_TYPE") объявлена только в docker-compose файле.
# Если она есть, значит запуск происходит через Docker. Иначе - локальный запуск.
if os.getenv("RUN_TYPE") == "docker":
    settings = DockerSettings()
else:
    settings = LocalSettings()
