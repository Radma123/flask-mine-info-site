from flask import Blueprint, abort, current_app, redirect, render_template, request, send_from_directory
from flask_login import current_user, login_required

index = Blueprint('index', __name__)

@index.route('/', methods = ['POST', 'GET'])
def index_page():
    return render_template('main/index.html')

@index.route('/robots.txt')
def robots():
    return send_from_directory(current_app.config['ROOT'], 'robots.txt')
