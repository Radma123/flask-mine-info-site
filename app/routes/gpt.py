from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from ..functions import get_all_gpts, gpt_send_message, save_picture, generate_img
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

    
@gpt.route("/gpt/create_chat", methods=["POST"])
def create_chat():
    try:
        # Получаем данные из запроса
        data = request.get_json()

        user_id = current_user.id
        print(user_id)
        print(1)
        model = data.get("model")
        user_message, bot_message = data.get("user_message"), data.get("bot_message")
        
        chat= Chats(user_id = user_id, model = model, first_message = user_message[:100])
        db.session.add(chat)
        db.session.commit()

        chat_id = Chats.query.filter_by(user_id = user_id).order_by(desc(Chats.date)).first().id
        usr_message = Messages(chat_id = chat_id, sender='user', message = user_message)
        db.session.add(usr_message)
        db.session.commit()
        bot_message = Messages(chat_id = chat_id, sender='bot', message = bot_message)
        db.session.add(bot_message)
        db.session.commit()

        

        return jsonify({
            "status": "success",
            "chat_id": f"{chat_id}"
        }), 200
        

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

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
    
@gpt.route("/gpt/<uuid:chat_id>/add", methods=["POST"])
@login_required
def add_to_chat(chat_id):
    if str(current_user.id) == Chats.query.filter_by(id = str(chat_id)).first().user_id:
        data = request.get_json()
        model = data.get("model")
        user_message, bot_message = data.get("user_message"), data.get("bot_message")

        Chats.query.filter_by(id = str(chat_id)).first().model = model
        db.session.commit()


        usr_message = Messages(chat_id = chat_id, sender='user', message = user_message)
        db.session.add(usr_message)
        db.session.commit()
        bot_message = Messages(chat_id = chat_id, sender='bot', message = bot_message)
        db.session.add(bot_message)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message" : "Message added to db"
        }), 200
    
    else:
        abort(403)

@gpt.route('/uploads/temp/<filename>', methods=['GET'])
def get_uploaded_temp(filename):
    """Возвращает загруженное временное фото по его имени"""
    return send_from_directory(current_app.config['UPLOAD_TEMP_PATH'], filename)

@gpt.route('/uploads/temp/<filename>', methods=['GET'])
@login_required
def get_uploaded_private(filename):
    """Возвращает загруженное приватное фото по его имени"""
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)

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
        photo = request.files.get("photo") #'base64_url'

        #user_info (protected)
        authenticated = current_user.is_authenticated
        user_id = current_user.id if authenticated else None

        print(1)
        print(request.form)

        if photo and photo.filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS_PHOTOS']: #вопрос с фото или без
            if current_user.is_authenticated:
                photo_path = save_picture(photo, temp=False)
                url = url_for('gpt.get_uploaded_private', filename=photo_path, _external=True)
                
            else:
                photo_path = save_picture(photo, temp=True)
                url = url_for('gpt.get_uploaded_temp', filename=photo_path, _external=True)
        elif generate_img_mode: #генерация фото
            bot_url = generate_img(user_message, model)
        else:
            raise Exception("No photo or generate_img_mode found")
        
        message = gpt_send_message(user_message, model, url)

        print(message)

        return jsonify({
            "status": "success",
            "message": message,
            "bot_url": bot_url if bot_url else None
        }), 200
        

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500