from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user
from ..extensions import db, bcrypt
from ..models.user import User
from ..forms import RegistrationForm, LoginForm
from ..functions import save_picture

storage = Blueprint('storage', __name__)

@storage.route('/storage', methods = ['POST', 'GET'])
def storage_page():
    return 'In devolopment', 200