FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/code

RUN mkdir $HOME
RUN mkdir $HOME/staticfiles
WORKDIR $HOME

RUN apt-get update && apt-get upgrade -y && apt-get install -y libsqlite3-dev libpq-dev build-essential python3-dev libldap2-dev libsasl2-dev ldap-utils tox lcov valgrind  
RUN pip install -U pip setuptools
RUN pip install virtualenv
RUN python -m virtualenv venv

COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

ADD . /code/
EXPOSE 8000
