
import os
from flask import Flask
from flask_cors import CORS 

from .config import config_map
from .extensions import db, bcrypt, login_manager, mail, jwt
from .models.user import User
from .controllers.api import api_bp
from .controllers.metadata_controller import metadata_bp
from .models.token_blocklist import TokenBlocklist


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
    jwt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'api.login_api'
    login_manager.login_message_category = 'info'
    
    # --- ADICIONE ESTE BLOCO DE CÓDIGO ---
    # Este "callback" é uma função que o JWT executa
    # toda vez que recebe um token, para checar se ele está na blocklist.
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    # 3. Registro dos Blueprints (Rotas)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(metadata_bp, url_prefix='/api/metadata')


    # 4. Cria tabelas no contexto do aplicativo
    with app.app_context():
        db.create_all()

    return app