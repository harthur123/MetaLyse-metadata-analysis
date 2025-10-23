# src/controllers/home_controller.py

from flask import jsonify # type: ignore
from src.services.auth_service import check_session # type: ignore

def home_route(user_token: str = None, action: str = None):
    """
    Endpoint da Tela de Início (API).
    Retorna mensagens e próximos passos em formato JSON.
    """
    try:
        is_authenticated = check_session(user_token)

        if action == "upload":
            if not is_authenticated:
                return jsonify({
                    "status": "error",
                    "redirect": "/login",
                    "message": "Faça login ou cadastre-se para continuar."
                }), 401
            else:
                return jsonify({
                    "status": "success",
                    "redirect": "/upload"
                }), 200

        # Tela inicial (apenas informações de boas-vindas)
        return jsonify({
            "status": "success",
            "message": "Bem-vindo ao MetaLyse — Analise seus arquivos e descubra seus metadados!",
            "authenticated": is_authenticated
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro no servidor: {e}"
        }), 500
