from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from ..functions import get_all_gpts, gpt_send_message, save_picture, generate_img, create_chat, add_to_chat, compress_base64
from ..extensions import client, db
from ..models.user import User, Chats, Messages
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import markdown

gpt = Blueprint('gpt', __name__)

@gpt.route('/gpt', methods = ['POST', 'GET'])
def gpt_page():
    gpts = get_all_gpts()
    if current_user.is_authenticated:
        choice_elements = Chats.query.filter_by(user_id = current_user.id).order_by(desc(Chats.date)).all()
        return render_template('gpt/gpt_page.html',gpts=gpts, choice_elements = choice_elements)
    else:
        return render_template('gpt/gpt_page.html',gpts=gpts)

    

@gpt.route("/gpt/<uuid:chat_id>", methods=["GET"])
@login_required
def chat(chat_id):
    if str(current_user.id) == Chats.query.filter_by(id = str(chat_id)).first().user_id:
        gpts = get_all_gpts()
        choice_elements = Chats.query.filter_by(user_id = current_user.id).order_by(desc(Chats.date)).all()
        model = Chats.query.filter_by(id = str(chat_id)).first().model

        messages = Messages.query.filter_by(chat_id = str(chat_id)).all()
        for message in messages:
            if message.message:
                message.message = markdown.markdown(message.message, extensions=['fenced_code'])


        return render_template('gpt/gpt_page.html',gpts=gpts, choice_elements = choice_elements, model=model, messages=messages)
    
    else:
        abort(403)

@gpt.route("/gpt/<uuid:chat_id>/delete", methods=["GET"])
@login_required
def delete_chat(chat_id):
    if str(current_user.id) == Chats.query.filter_by(id = str(chat_id)).first().user_id:
        remove_chat = Chats.query.filter_by(id = str(chat_id)).first()
        db.session.delete(remove_chat)
        db.session.commit()


        return redirect("/gpt")
    
    else:
        abort(403)
    

@gpt.route('/uploads/temp/<filename>', methods=['GET'])
def get_uploaded_temp(filename):
    """Возвращает загруженное временное фото по его имени"""
    return send_from_directory(current_app.config['UPLOAD_TEMP_PATH'], filename)

@gpt.route('/uploads/<filename>', methods=['GET'])
@login_required
def get_uploaded_private(filename):
    """Возвращает загруженное приватное фото по его имени"""
    if current_user.id == Messages.query.filter_by(media = filename).first().user_id:
        return send_from_directory(current_app.config['UPLOAD_PATH'], filename)
    abort(403)


@gpt.route("/send", methods=["POST"])
def send():
    try:
        # general info
        model = request.form.get("gpt") #'gpt'
        generate_img_mode = request.form.get("generate_img_mode") #'true'/'false'
        database_mode = request.form.get("database_mode") #'guest/create_chat/add_to_chat'
        chat_id = request.form.get("chat_id") #'chat_id'

        #messages
        user_message = request.form.get("user_message") #'text'
        photo = request.files.get("photo") #'bytes'

        #user_info (protected)
        authenticated = current_user.is_authenticated
        user_id = current_user.id if authenticated else None

        photo_base64 = None
        bot_url = None
        message = None
        chat_url = None
        photo_path = None
        bot_photo_path = None
        #Данные________________________________________________________________________________________________
        if photo != None and photo.filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS_PHOTOS']: #вопрос с фото или без
            photo_base64 = compress_base64(photo.read()) #base64 -> compressed base64

        if generate_img_mode == 'true': #генерация фото
                bot_url = generate_img(user_message, model) #base64
        else:
            message = gpt_send_message(user_message, model, photo_base64=photo_base64)

        if authenticated:
            if bot_url:
                bot_photo_path = save_picture(bot_url, temp=False, img_type='base64')
            if photo_base64:
                photo_path = save_picture(photo_base64, temp=False, img_type='base64')
            match database_mode:
                case 'create_chat':
                    chat_url = create_chat(user_id=user_id, model=model, user_message=user_message, photo_path=photo_path, message=message, bot_photo_path=bot_photo_path)
                case 'add_to_chat':
                    add_to_chat(chat_id=chat_id, user_id=user_id, model=model, user_message=user_message, photo_path=photo_path, message=message, bot_photo_path=bot_photo_path)
                case _:
                    pass
                

        return jsonify({
            "status": "success",
            "message": markdown.markdown(message, extensions=['fenced_code']),
            "bot_url": bot_url,
            "redirection": chat_url
        }), 200
        

    except Exception as e:
        current_app.logger.error(f"Ошибка обработки сообщения: {str(e)}", exc_info=True)

        return jsonify({
            "status": "error",
            "message": 'Server Error'
        }), 500
