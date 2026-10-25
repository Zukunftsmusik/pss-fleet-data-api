# The builder image, used to build the virtual environment
FROM python:3.13.17-slim AS runtime

WORKDIR /app

RUN useradd --system --uid 10001 --create-home app
RUN PYTHONDONTWRITEBYTECODE=1 python -m pip install --no-cache-dir --upgrade "pip==26.2.2"

COPY requirements.txt ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app alembic.ini ./alembic.ini
COPY --chown=app:app src ./src

USER app

ENTRYPOINT ["fastapi", "run", "src/api/main.py", "--port", "80"]