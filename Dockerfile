FROM python:3.6

WORKDIR /app
ARG requirements=requirements/production.txt

ADD . /app

RUN pip install -e .
RUN pip install -r $requirements
