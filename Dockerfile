FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /geo-polygons
COPY poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}
COPY . .

WORKDIR src
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
