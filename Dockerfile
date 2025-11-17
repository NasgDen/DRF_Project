FROM python:3.13

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

EXPOSE 8000
