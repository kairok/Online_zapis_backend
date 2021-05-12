FROM python:3.6
ENV PYTHONUNBUFFERED 1
ADD . /srv/app
WORKDIR /srv/app
COPY . /srv/app


RUN pip install -r requirements.txt




