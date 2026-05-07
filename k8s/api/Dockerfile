FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
COPY ./src ./src

RUN uv sync -n --group api

EXPOSE 8080

ENTRYPOINT ["uv", "-n", "run", "--no-sync", "python", "src/titanic/api/main.py"]
