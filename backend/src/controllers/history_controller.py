from flask import Blueprint, jsonify, request
from ..services import history_service  
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.decorators import admin_required 

history_bp = Blueprint('history_bp', __name__)

@history_bp.route('/my-history', methods=['GET'])
@jwt_required()
def get_my_history_route():
    """Retorna o histórico do usuário que está logado."""
    try:
        user_id = get_jwt_identity()
        data = history_service.get_history_by_user_id(user_id)
        return jsonify({
            "status": "success",
            "historico": data
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@history_bp.route('/all-history', methods=['GET'])
@admin_required()  # <-- Protegido! Só admin pode ver.
def get_all_history_route():
    """Retorna TODO o histórico de TODOS os usuários."""
    try:
        data = history_service.get_all_history()
        return jsonify({
            "status": "success",
            "historico": data
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@history_bp.route('/save', methods=['POST'])
@jwt_required()
def save_history_route():
    """Salva uma nova entrada de histórico para o usuário logado."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        file_name = data.get("file_name")
        file_type = data.get("file_type")

        if not file_name or not file_type:
            return jsonify({"status": "error", "message": "file_name e file_type são obrigatórios"}), 400

        record = history_service.add_history(file_name, file_type, user_id)
        
        return jsonify({
            "status": "success",
            "registro": record
        }), 201 
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500