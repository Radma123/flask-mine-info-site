from io import BytesIO
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

    return chat_id


# @gpt.route("/gpt/<uuid:chat_id>/add", methods=["POST"])
# @login_required
# def add_to_chat(chat_id):
#     if str(current_user.id) == Chats.query.filter_by(id = str(chat_id)).first().user_id:
#         data = request.get_json()
#         model = data.get("model")
#         user_message, bot_message = data.get("user_message"), data.get("bot_message")

#         Chats.query.filter_by(id = str(chat_id)).first().model = model
#         db.session.commit()


#         usr_message = Messages(chat_id = chat_id, sender='user', message = user_message)
#         db.session.add(usr_message)
#         db.session.commit()
#         bot_message = Messages(chat_id = chat_id, sender='bot', message = bot_message)
#         db.session.add(bot_message)
#         db.session.commit()

#         return jsonify({
#             "status": "success",
#             "message" : "Message added to db"
#         }), 200
    
#     else:
#         abort(403)


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