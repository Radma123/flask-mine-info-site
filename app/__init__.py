from flask import Flask
from .bundles import bundles, register_bundles
from .extensions import db,migrate, bcrypt, assets
from .config import Config
from .routes.index import index

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(index)

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
    register_bundles(assets, bundles)

    with app.app_context():
        db.create_all()

    return app