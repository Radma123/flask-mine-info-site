from g4f import models
import secrets
import os
from flask import current_app
from PIL import Image

def get_all_gpts() -> list:
    gpts = models._all_models

    return gpts

def safe_picture(picture):
    if not picture:
        return ''

    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.config['SERVER_PATH'], picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn