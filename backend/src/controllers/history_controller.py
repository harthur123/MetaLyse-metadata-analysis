from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..services.history_service import HistoryService

history_bp = Blueprint('history', __name__)
service = HistoryService()

# --- ROTA DE USUÁRIO (Ver o próprio histórico) ---
@history_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_history():
    user_id = get_jwt_identity()
    search = request.args.get('search') # Pega ?search=termo da URL
    
    try:
        results = service.get_history(user_id=user_id, search_term=search, is_admin=False)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROTA DE ADMIN (Ver tudo) ---
@history_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_history():
    user_id = get_jwt_identity()
    
    # Verifica se é Admin (A.1 do Admin)
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({"message": "Acesso negado. Requer privilégios de administrador."}), 403

    search = request.args.get('search')
    
    try:
        results = service.get_history(user_id=None, search_term=search, is_admin=True)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROTA DE DETALHES (Para expandir ou exportar) ---
@history_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_history_details(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    is_admin = (user and user.role == 'admin')

    result = service.get_by_id(id, user_id, is_admin)
    
    if not result:
        return jsonify({"message": "Registro não encontrado ou acesso não autorizado."}), 404
        
    return jsonify(result), 200