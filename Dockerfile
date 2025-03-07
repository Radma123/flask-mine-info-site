FROM python:3.12.3

WORKDIR /app

ADD . /app

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
RUN apt-get update --fix-missing && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "flask db migrate && flask db migrate && flask db upgrade && uwsgi app.ini"]
