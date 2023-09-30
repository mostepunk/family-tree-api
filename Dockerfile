FROM python:3.10-slim as builder

MAINTAINER Mostepan.VI
LABEL version="0.0"

ENV PYTHONUNBUFFERED=1
ENV TZ Europe/Moscow
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .

# ENTRYPOINT bash -c "uvicorn family.application:app --host 0.0.0.0 --port 80 --reload"
ENTRYPOINT bash -c "uvicorn main:app --host 0.0.0.0 --port 80 --reload"
# ENTRYPOINT bash -c "python main.py"
