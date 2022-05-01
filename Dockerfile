FROM whoiskp/python:lus-base

COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

WORKDIR /webapps

COPY . /webapps