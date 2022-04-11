FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/places_remember/places_remember_back/

RUN apt-get update && apt-get -y install --no-install-recommends \
        build-essential \
        python3 python3-setuptools python3-pip \
        postgresql-13 postgresql-client-13 \
        postgis postgresql-13-postgis-3 postgresql-13-postgis-3-scripts \
        libproj-dev proj-data python3-gdal proj-bin libgeos-dev gdal-bin

ENV DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_PASSWORD=admin

COPY requirements.txt /usr/src/places_remember/places_remember_back/

RUN pip3 install pip --upgrade && pip3 install -r /usr/src/places_remember/places_remember_back/requirements.txt

COPY . /usr/src/places_remember/places_remember_back/


EXPOSE 8000