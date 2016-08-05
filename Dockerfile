FROM python:2.7.11-alpine

RUN apk update && apk add ca-certificates

ADD . /sdk
WORKDIR sdk
RUN python setup.py install

