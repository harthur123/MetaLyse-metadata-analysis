
import os
from flask import Flask
from flask_cors import CORS 

from .config import config_map
from .extensions import db, bcrypt, login_manager, mail
from .models.user import User
from .models.history import History
from .controllers.api import api_bp


def create_app(config_name='default'):
    app = Flask(__name__)

    # Permite que o 'http://localhost:4200' (Angular)
    # acesse os recursos da sua API (rotas que começam com /api/)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

    # 1. Configuração da Aplicação
    app.config.from_object(config_map[config_name])

    # 2. Inicialização das Extensões
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'api.login_api'
    login_manager.login_message_category = 'info'

    # 3. Registro dos Blueprints (Rotas)
    app.register_blueprint(api_bp, url_prefix='/api')


    # 4. Cria tabelas no contexto do aplicativo
    with app.app_context():
        db.create_all()

    return app