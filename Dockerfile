# The builder image, used to build the virtual environment
FROM python:3.13.17-slim AS runtime

WORKDIR /app

RUN PYTHONDONTWRITEBYTECODE=1 python -m pip install --no-cache-dir --upgrade "pip==26.2.2"

COPY requirements.txt ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.txt

COPY alembic.ini ./alembic.ini
COPY src ./src

ENTRYPOINT ["fastapi", "run", "src/api/main.py", "--port", "80"]