FROM python:3.6.1

MAINTAINER Daniel Soria <@azhtom>

WORKDIR /usr/src/app

COPY iblups/requirements.txt ./
RUN pip install -r requirements.txt

COPY iblups .