import uuid
from datetime import datetime, timezone
from ..extensions import db, login_manager
from flask_login import UserMixin
import os
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.String(50), nullable=False, default='user')

    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(250))

    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Chats(db.Model):
    __tablename__ = 'chats'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    first_message = db.Column(db.String(100))

    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @staticmethod
    def before_delete(mapper, connection, target):
        """Обработчик событий для удаления чатов."""
        print(f"Удаление чата с ID: {target.id}")
        # Получаем все сообщения, связанные с этим чатом, и удаляем файлы
        messages = Messages.query.filter_by(chat_id=target.id).all()
        for message in messages:
            message.delete_file()


class Messages(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = db.Column(db.String, db.ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    sender = db.Column(db.String(40), nullable=False)
    message = db.Column(db.String(4096))
    media = db.Column(db.String(200))

    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def delete_file(self):
        """Удаляет файл с диска перед удалением записи из БД."""
        if self.media is None:
            return
        
        file_path = os.path.join(current_app.config['UPLOAD_PATH'], self.media)
        print(f"Пытаемся удалить файл: {file_path}")
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Файл удалён")
        else:
            print(f"Файл не найден: {file_path}")