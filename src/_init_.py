# Em src/__init__.py

from flask import Flask
from flask_cors import CORS
# Importe aqui as outras extensões (SQLAlchemy, JWT, etc.) quando instalá-las

def create_app():
    """
    Esta é a "Application Factory". 
    Ela constrói e configura a instância do app Flask.
    """
    app = Flask(__name__)
    
    # Quando tiver o config.py, você vai usar:
    # app.config.from_object('config.Config') 
    
    # Habilita o CORS para o seu Angular poder se comunicar
    CORS(app) 
 
    # --- Registro dos Blueprints (seus controllers) ---
    # Usamos o '.' para importação relativa, já que estamos dentro do pacote 'src'
    from .controllers.history_controller import history_bp
    from .controllers.home_controller import home_bp
    from .controllers.metadata_controller import metadata_bp

    # Registra os blueprints na aplicação
    # O 'url_prefix' adiciona /api antes de todas as rotas daquele controller
    app.register_blueprint(history_bp, url_prefix='/api/history')
    app.register_blueprint(home_bp, url_prefix='/api/home')
    app.register_blueprint(metadata_bp, url_prefix='/api/metadata')
 
    return app