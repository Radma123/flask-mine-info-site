from flask import Flask
from .extensions import db,migrate, bcrypt, assets
from .config import Config
from .routes.index import index
from .routes.gpt import gpt
from flask_assets import Bundle

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(index)
    app.register_blueprint(gpt)

    #INIT APP
    db.init_app(app)
    migrate.init_app(app, db)
    # login_manager.init_app(app)
    bcrypt.init_app(app)
    assets.init_app(app)

    #LOGIN MANAGER
    # login_manager.login_view = 'user.login'
    # login_manager.login_message = 'Вы не можете перейти на эту страницу без авторизации'
    # login_manager.login_message_category = 'info'
    
    #ASSETS
    # js_bundle = Bundle('css/*.css', filters='cssmin', output='gen/css/style.min.css')
    # css_bundle = Bundle('js/*.js', filters='jsmin', output='gen/js/app.min.js')
    # assets.register('css_all', css_bundle)
    # assets.register('js_all', js_bundle)

    
    with app.app_context():
        db.create_all()

    return app