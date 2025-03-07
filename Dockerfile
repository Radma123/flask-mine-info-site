FROM python:3.12.3

WORKDIR /app

ADD . /app

RUN apt-get update --fix-missing && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "flask db init && flask db migrate && flask db upgrade && uwsgi app.ini"]
