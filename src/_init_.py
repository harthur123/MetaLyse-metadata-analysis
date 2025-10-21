from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config # Importa a classe Config

# Crie as instâncias das extensões AQUI, sem app
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicialize as extensões AQUI, com o app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app) # Permite o Angular se conectar

    # --- Importar e Registrar Blueprints ---
    from .controllers.auth_controller import auth_bp
    from .controllers.history_controller import history_bp
    # Importe seus outros controllers (home, metadata) aqui...

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    # Registre seus outros blueprints aqui...

    # Importa os modelos para que o 'migrate' os veja
    from .models import User, history

    return app