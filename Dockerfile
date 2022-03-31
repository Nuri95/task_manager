FROM python:3.8

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/root/.poetry/bin:$PATH"

COPY pyproject.toml .
RUN poetry install --system

COPY ./src ./src
COPY .env .
COPY init.sh init.sh

EXPOSE 8000

CMD ["sh", "init.sh"]