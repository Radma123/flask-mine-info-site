from flask import Blueprint, abort, jsonify, redirect, render_template, request
from flask_login import current_user, login_required
from ..functions import get_all_gpts
from ..extensions import client

gpt = Blueprint('gpt', __name__)

@gpt.route('/gpt', methods = ['POST', 'GET'])
def gpt_page():

    gpts = get_all_gpts()
    return render_template('gpt/gpt_page.html',gpts=gpts)

@gpt.route("/send", methods=["POST"])
def send():
    print('a')
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