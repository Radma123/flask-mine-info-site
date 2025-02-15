from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user
from ..extensions import db, bcrypt
from ..models.user import User
from ..forms import RegistrationForm, LoginForm
from ..functions import save_avatar_picture

user = Blueprint('user', __name__)

@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        avatar_filename = save_avatar_picture(form.avatar.data)
        user = User(username = form.username.data, avatar = avatar_filename, password = hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Registration Successfull", "success")
            return redirect(url_for('user.login'))
        except Exception as err:
            print(err)
            flash(f"Registration Error", "danger")  
    return render_template('user/register.html', form=form) 

@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            flash(f"Welcome, {user.username}!", "success")
            return redirect(next_page) if next_page else redirect(url_for('index.index_page'))
        else:
            flash(f"Error", "danger")
    return render_template('user/login.html', form=form) 
        
@user.route('/user/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index.index_page'))