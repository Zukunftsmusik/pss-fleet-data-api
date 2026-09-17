# The builder image, used to build the virtual environment
FROM python:3.12.3-slim AS runtime

WORKDIR /app

COPY requirements.txt ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.txt

COPY alembic.ini ./alembic.ini
COPY src ./src

ENTRYPOINT ["fastapi", "run", "src/api/main.py", "--port", "80"]