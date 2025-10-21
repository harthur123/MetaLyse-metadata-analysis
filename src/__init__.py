# src/__init__.py (Corrigido)

import os
from flask import Flask

from .config import config_map
from .extensions import db, bcrypt, login_manager, mail
from .models.user import User
from .models.history import History
# CORREÇÃO: Importa o nome correto do Blueprint da API, que é 'api_bp'
from .controllers.api import api_bp


def create_app(config_name='default'):
    """Função factory para criar a instância da aplicação Flask."""
    app = Flask(__name__)

    # 1. Configuração da Aplicação
    # Carrega a configuração específica (development, production ou default)
    app.config.from_object(config_map[config_name])

    # 2. Inicialização das Extensões
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    login_manager.init_app(app)
    # Define a view de login apontando para o endpoint da API
    login_manager.login_view = 'api.login_api'
    login_manager.login_message_category = 'info'

    # 3. Registro dos Blueprints (Rotas)
    # Registra o Blueprint da API com o nome correto
    app.register_blueprint(api_bp)

    # 4. Cria tabelas no contexto do aplicativo (necessário para SQLite/desenvolvimento)
    with app.app_context():
        db.create_all()

    return app