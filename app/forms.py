from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, PasswordField, SelectField, StringField, SubmitField, ValidationError
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo

from .models.user import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Enter')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password again', validators=[DataRequired(), EqualTo('password')])
    avatar = FileField('Avatar(not necessary)', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This name is occupied')