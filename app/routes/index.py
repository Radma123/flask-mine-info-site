from flask import Blueprint, abort, redirect, render_template, request
from flask_login import current_user, login_required

index = Blueprint('index', __name__)

@index.route('/', methods = ['POST', 'GET'])
def index_page():
    return render_template('main/index.html')
