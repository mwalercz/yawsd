FROM python:3.6.1-alpine

RUN apk update \
    && apk add gcc libffi-dev openssl-dev python3-dev \
    musl-dev postgresql-dev make

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements_dev.txt /usr/src/app/
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY ./docker/entrypoint.sh /usr/bin/entrypoint
RUN chmod 755 /usr/bin/entrypoint
ENTRYPOINT ["entrypoint"]



