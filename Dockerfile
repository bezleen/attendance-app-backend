FROM python:3.8-alpine

COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

WORKDIR /webapps

COPY . /webapps