from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv('.env')
load_dotenv('.flaskenv')

os.environ.update({
    'FLASK_ENV': 'development',
    'FLASK_DEBUG': 'True',
    'POSTGRES_HOST': '127.0.0.1'
})

from app.config import Config
print(Config.HOST)

# Импортирование create_app после конфигурации
from app import create_app

# Создание приложения
application = create_app()


if __name__ == '__main__':
    application.run()
