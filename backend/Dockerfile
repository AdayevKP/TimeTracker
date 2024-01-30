FROM python:3.12

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    # this flag for installing all deps to system python
    && poetry config virtualenvs.create false 
RUN poetry install

COPY ./app .

EXPOSE 80

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]