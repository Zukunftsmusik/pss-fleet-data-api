# The builder image, used to build the virtual environment
FROM python:3.12.3-slim as runtime

WORKDIR /app

COPY requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY src ./src

ENTRYPOINT ["fastapi", "run", "app/src/main.py", "--port", "80"]