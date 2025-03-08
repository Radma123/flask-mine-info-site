FROM python:3.12.3

WORKDIR /app

ADD . /app

RUN apt-get update --fix-missing && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт в контейнер
COPY entrypoint.sh /entrypoint.sh

# Делаем его исполняемым
RUN chmod +x /entrypoint.sh

# Устанавливаем точку входа
ENTRYPOINT ["/entrypoint.sh"]
