FROM python:3.5.3-alpine

RUN apk update && apk add ca-certificates

ADD . /sdk
WORKDIR sdk
RUN python setup.py install

