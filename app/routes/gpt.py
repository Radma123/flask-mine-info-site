from flask import Blueprint, abort, jsonify, redirect, render_template, request
from flask_login import current_user, login_required
from ..functions import get_all_gpts
from ..extensions import client, db
from ..models.user import User, Chats, Messages
from sqlalchemy import desc

gpt = Blueprint('gpt', __name__)

@gpt.route('/gpt', methods = ['POST', 'GET'])
def gpt_page():
    gpts = get_all_gpts()
    if current_user.is_authenticated:
        choice_elements = Chats.query.filter_by(user_id = current_user.id).order_by(desc(Chats.date)).all()
        return render_template('gpt/gpt_page.html',gpts=gpts, choice_elements = choice_elements)
    else:
        return render_template('gpt/gpt_page.html',gpts=gpts)

@gpt.route("/send", methods=["POST"])
def send():
    try:
        # Получаем данные из запроса
        data = request.get_json()

        prompt = data.get("text")
        model = data.get("gpt")

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            web_search=False
        )

        print(response.choices[0].message.content)

        return jsonify({
            "status": "success",
            "message": response.choices[0].message.content
        }), 200
        

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
# @gpt.route(f'/gpt/{}', methods = ['POST', 'GET'])
# def chat():

#     gpts = get_all_gpts()
#     return render_template('gpt/gpt_page.html',gpts=gpts)

@gpt.route("/create_chat", methods=["POST"])
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
        # messages


        return render_template('gpt/gpt_page.html',gpts=gpts, choice_elements = choice_elements, model=model)
    
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