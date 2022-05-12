FROM whoiskp/python:lus-base

COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt
RUN pip --no-cache-dir install pyrebase==3.0.27
RUN pip --no-cache-dir install pycryptodome==3.11.0
RUN pip --no-cache-dir install requests==2.25.1


WORKDIR /webapps

COPY . /webapps