from flask import Blueprint, abort, redirect, render_template, request
from flask_login import current_user, login_required
from ..functions import get_all_gpts

gpt = Blueprint('gpt', __name__)

@gpt.route('/gpt', methods = ['POST', 'GET'])
def gpt_page():

    # gpts = get_all_gpts()
    return render_template('gpt/gpt_page.html')