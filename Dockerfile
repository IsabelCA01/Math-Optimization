FROM python:3.10.12-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN apt update

RUN python -m pip install --upgrade pip

RUN pip install pipenv==2023.6.12

COPY Pipfile* ./

RUN pipenv install --deploy --system

COPY . .

CMD ["python3", "opt-101.py"]

