from flask import Blueprint, jsonify

# --- 1. IMPORTAR OS BLUEPRINTS "FILHOS" ---
from .auth_controller import auth_bp
# A LINHA DO ERRO ESTÁ AQUI (agora vai funcionar se o passo 1 estiver correto)
from .metadata_controller import metadata_bp 

from .history_controller import history_bp


# --- 2. CRIAR O BLUEPRINT "PAI" DA API ---
api_bp = Blueprint('api', __name__, url_prefix='/api')


# --- 3. REGISTRAR OS BLUEPRINTS "FILHOS" DENTRO DO "PAI" ---
api_bp.register_blueprint(auth_bp, url_prefix='/auth')
# GARANTA QUE ESTA LINHA ESTEJA AQUI E DESCOMENTADA:
api_bp.register_blueprint(metadata_bp, url_prefix='/metadata')
api_bp.register_blueprint(history_bp, url_prefix='/history')


# --- 4. MANTER APENAS A ROTA DE STATUS ---
@api_bp.route("/status", methods=["GET"])
def get_status():
    """Rota para o Angular verificar se a API está online."""
    return jsonify({"status": "API online"}), 200
