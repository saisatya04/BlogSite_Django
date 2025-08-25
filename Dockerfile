FROM python:3.13-bullseye AS base
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install gettext -y

RUN mkdir /code
WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

FROM base AS development

RUN poetry install --no-root

RUN poetry run playwright install --with-deps

COPY . .
RUN chmod 755 /code/start-django.sh

EXPOSE 8000

ENTRYPOINT [ "/code/start-django.sh" ]

# ENTRYPOINT [ ""poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"" ]
# The above entrypoint is re-written after the command is written in the start-django.sh file


FROM base AS production

RUN poetry install --only main --no-root

COPY . .
RUN chmod 755 /code/start-django.sh

EXPOSE 8000

ENTRYPOINT [ "/code/start-django.sh" ]
