FROM python:2.7.11-alpine

ADD . /sdk
WORKDIR sdk
RUN python setup.py install

