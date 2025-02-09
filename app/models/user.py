import uuid
from datetime import datetime, timezone
from ..extensions import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.String(50), default='user')

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


class Messages(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = db.Column(db.String, db.ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    sender = db.Column(db.String(40), nullable=False)
    message = db.Column(db.String(4096), nullable=False)

    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
