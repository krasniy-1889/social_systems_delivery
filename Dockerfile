# тут можно поставить версию slim или alpine. Но нужно проверять. Poetry не всегда работает
FROM python:3.12-alpine


WORKDIR /code

COPY /pyproject.toml /code
COPY /poetry.lock  /code

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . .

EXPOSE 8000


ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
