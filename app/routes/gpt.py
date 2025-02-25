from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from ..functions import get_all_gpts, gpt_send_message, save_picture, generate_img, create_chat, add_to_chat
from ..extensions import client, db
from ..models.user import User, Chats, Messages
from sqlalchemy import desc
from werkzeug.utils import secure_filename

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

# @gpt.route("/gpt/upload", methods=["POST"])
# def upload():
#     try:
#         # Получаем файл из запроса
#         uploaded_file = request.files.get("file")

#         if not uploaded_file:
#             return jsonify({
#                 "status": "error",
#                 "message": "Файл не был загружен"
#             }), 400


#         with open(current_app.config['SERVER_PATH']+uploaded_file.filename, "wb") as f:
#             f.write(uploaded_file.read())

#         return jsonify({
#             "status": "success",
#             "message": uploaded_file.filename
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

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

        url = None
        bot_url = None
        message = None
        chat_url = None
        photo_path = None
        bot_photo_path = None
        #Данные________________________________________________________________________________________________
        print(1)
        print(request.form)

        if photo != None and photo.filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS_PHOTOS']: #вопрос с фото или без
            print(2)
            photo_path = save_picture(photo, temp=True, img_type='img')
            url = url_for('gpt.get_uploaded_temp', filename=photo_path, _external=True)

        if generate_img_mode == 'true': #генерация фото
            if authenticated:
                print(11)
                generated_base64 = generate_img(user_message, model) #base64
                print(12)
                print(generated_base64)
                bot_photo_path = save_picture(generated_base64, temp=True, img_type='base64')
                print('-----------------')
                print(bot_photo_path)
                bot_url = url_for('gpt.get_uploaded_temp', filename=bot_photo_path, _external=True)
            else:
                bot_url = generate_img(user_message, model) #base64
        else:
            message = gpt_send_message(user_message, model, photo=url)

        print(3)
        print(message)

        if authenticated:
            match database_mode:
                case 'create_chat':
                    chat_url = create_chat(user_id=user_id, model=model, user_message=user_message, photo_path=photo_path, message=message, bot_photo_path=bot_photo_path)
                case 'add_to_chat':
                    add_to_chat(chat_id=chat_id, user_id=user_id, model=model, user_message=user_message, photo_path=photo_path, message=message, bot_photo_path=bot_photo_path)
                case _:
                    pass
                

        return jsonify({
            "status": "success",
            "message": message,
            "bot_url": bot_url,
            "redirection": chat_url
        }), 200
        

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500