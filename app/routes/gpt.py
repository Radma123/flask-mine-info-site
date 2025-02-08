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

        user_id = data.get("user_id")
        model = data.get("model")
        user_message, bot_message = data.get("user_message"), data.get("bot_message")
        
        chat= Chats(user_id = user_id, model = model)
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
            "message": "Chat created successfully!"
        }), 200
        

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500