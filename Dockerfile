FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
COPY ./requirements.txt /app

RUN apt update
RUN apt install -y python3-opencv
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt