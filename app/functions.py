from io import BytesIO
import logging
from g4f import models
import secrets
import os
from flask import current_app
from PIL import Image
from .extensions import client, db
from .models.user import User, Chats, Messages
from sqlalchemy import desc
import base64

def get_all_gpts() -> list:
    gpts = models._all_models

    return gpts

#возвращает ЧИСТЫЙ base64 лбрезанный
def compress_base64(base64_string, max_size=(1024, 1024)):
    base64_string = base64_string.split(' ')[-1]
    img_bytes = base64.b64decode(base64_string)

    i = Image.open(BytesIO(img_bytes))
    i.thumbnail(max_size)

    buffer = BytesIO()
    i.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode()


def gpt_send_message(prompt, model, photo=None):
    messages = [{"role": "user", "content": prompt}]
    
    if photo != None:
        # print(photo)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": photo}}
                ]
            }
        ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        web_search=False
    )

    return response.choices[0].message.content

def generate_img(prompt, model):
    response = client.images.generate(
        model=model,
        prompt=prompt,
        response_format="b64_json"
    )
    
    return f'data:image/png;base64, {response.data[0].b64_json}'

def create_chat(user_id, model, user_message, photo_path=None, message=None, bot_photo_path=None):
    try:
        first_message = user_message[:100] if message else 'Your photo 🖼️'

        chat= Chats(user_id = user_id, model = model, first_message = first_message)
        db.session.add(chat)
        db.session.commit()

        chat_id = Chats.query.filter_by(user_id = user_id).order_by(desc(Chats.date)).first().id

        usr_message = Messages(chat_id = chat_id, user_id=user_id, sender='user', message = user_message, media=photo_path)
        db.session.add(usr_message)
        db.session.commit()
        message = Messages(chat_id = chat_id, user_id=user_id, sender='bot', message = message, media = bot_photo_path)
        db.session.add(message)
        db.session.commit()
        current_app.logger.info(f"Создание чата: {chat_id}")
        
        return chat_id
    except Exception as e:
        current_app.logger.error(f"Ошибка создания чата: {str(e)}", exc_info=True)

def add_to_chat(chat_id, user_id, model, user_message, photo_path=None, message=None, bot_photo_path=None):
    try:
        if user_id == Chats.query.filter_by(id = str(chat_id)).first().user_id:
            Chats.query.filter_by(id = str(chat_id)).first().model = model
            db.session.commit()

            usr_message = Messages(chat_id = chat_id, user_id=user_id, sender='user', message = user_message, media=photo_path)
            db.session.add(usr_message)
            db.session.commit()
            message = Messages(chat_id = chat_id, user_id=user_id, sender='bot', message = message, media = bot_photo_path)
            db.session.add(message)
            db.session.commit()
        else:
            raise Exception("Нельзя отправить сообщение другому пользователю")
    except Exception as e:
        current_app.logger.error(f"Ошибка добавления сообщения в чат: {str(e)}", exc_info=True)
        


def save_avatar_picture(picture):
    if not picture:
        return ''

    random_hex = secrets.token_hex(8)
    file_ext = os.path.splitext(picture.filename)[-1]
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.config['UPLOAD_PATH'], picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)

    if not os.path.exists(current_app.config['UPLOAD_PATH']):
        os.makedirs(current_app.config['UPLOAD_PATH']) 

    i.save(picture_path)
    return picture_fn

def save_picture(picture, img_type, temp=True):
    if not picture:
        return ''
    if not os.path.exists(current_app.config['UPLOAD_PATH']):
        os.makedirs(current_app.config['UPLOAD_PATH'])
    if not os.path.exists(current_app.config['UPLOAD_TEMP_PATH']):
        os.makedirs(current_app.config['UPLOAD_TEMP_PATH'])

    random_hex = secrets.token_hex(8)

    match img_type:
        case 'img':
            file_ext = os.path.splitext(picture.filename)[-1]
            picture_fn = random_hex + file_ext
        case 'base64':
            picture_fn = random_hex + '.webp'

    if temp == True:
        picture_path = os.path.join(current_app.config['UPLOAD_TEMP_PATH'], picture_fn)
    else:
        picture_path = os.path.join(current_app.config['UPLOAD_PATH'], picture_fn)

    match img_type:
        case 'img':
            i = Image.open(picture)
        case 'base64':
            base64_data = picture.split(' ')[-1] if ' ' in picture else picture
            img_bytes = base64.b64decode(base64_data)
            i = Image.open(BytesIO(img_bytes))
        
    i.save(picture_path)
    
    return picture_fn