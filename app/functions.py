from g4f import models
import secrets
import os
from flask import current_app
from PIL import Image
from .extensions import client

def get_all_gpts() -> list:
    gpts = models._all_models

    return gpts

def gpt_send_message(prompt, model, photo=None):
    messages = [{"role": "user", "content": prompt}]
    
    if photo:
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

def save_picture(picture, temp=True):
    if not picture:
        return ''
    
    random_hex = secrets.token_hex(16)
    file_ext = os.path.splitext(picture.filename)[-1]
    picture_fn = random_hex + file_ext

    if temp:
        picture_path = os.path.join(current_app.config['UPLOAD_TEMP_PATH'], picture_fn)

        if not os.path.exists(current_app.config['UPLOAD_TEMP_PATH']):
            os.makedirs(current_app.config['UPLOAD_TEMP_PATH'])
    else:
        picture_path = os.path.join(current_app.config['UPLOAD_PATH'], picture_fn)

        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])

    i = Image.open(picture)
    i.save(picture_path)
    
    return picture_fn