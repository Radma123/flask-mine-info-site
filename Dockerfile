FROM python:3.12.3

WORKDIR /app

ADD . /app

RUN apt install gcc -y && apt-get update --fix-missing
RUN pip install -r requirements.txt

CMD [ "uwsgi", "app.ini" ]