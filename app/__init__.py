from flask import Flask
from .extensions import db,migrate, bcrypt, assets, login_manager
from .config import Config

from .routes.index import index
from .routes.user import user
from .routes.gpt import gpt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(index)
    app.register_blueprint(user)
    app.register_blueprint(gpt)

    #INIT APP
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    assets.init_app(app)

    # LOGIN MANAGER
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Вы не можете перейти на эту страницу без авторизации'
    login_manager.login_message_category = 'info'


    @app.errorhandler(404)
    def page_not_found(e):
        return "Страница не найдена", 404


    
    with app.app_context():
        db.create_all()

    return app