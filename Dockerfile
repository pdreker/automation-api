# Pull the generated requirements.txt and install into system using pip
FROM python:3.11-alpine AS build
WORKDIR /app

RUN apk add build-base libffi-dev && \
    pip install --upgrade pip && \
    pip install poetry==1.4.0

COPY README.md /app/
COPY pyproject.toml /app
COPY poetry.lock /app
COPY automation_api /app/automation_api

RUN poetry build


FROM python:3.11-alpine
ENV PIP_NO_CACHE_DIR="true"
WORKDIR /app

COPY --from=build /app/dist/*.whl /

RUN pip install /*.whl && \
    rm /*.whl

ENTRYPOINT ["uvicorn", "automation_api:app", "--host", "0.0.0.0"]
