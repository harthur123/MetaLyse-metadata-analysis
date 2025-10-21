
from flask import jsonify, request
from services.history_service import get_all_history


def history_route():
    """
    Retorna todo o histórico de arquivos analisados
    """
    try:

        data = get_all_history()
        return jsonify({
            "status": "success",
            "historico": data
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao recuperar histórico: {e}"
        }), 500
    
def save_history_route():
    """
    Adiciona uma nova entrada ao histórico (chamado após uma análise)
    """

    try:
        data = request.get_json()
        file_name = data.get("file_name")
        file_type = data.get("file_type")
        user = data.get("user", "Anônimo")

        record = add_history(file_name, file_type, user)
        
        return jsonify({
            "status": "success",
            "registro": record
        }), 201
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao salvar histórico: {e}"
        }), 500