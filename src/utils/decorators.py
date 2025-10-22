# Em: src/utils/decorators.py

from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models.user import User  
from flask import jsonify

def admin_required():
    
    def wrapper(fn):
        @wraps(fn)
        @jwt_required() # 1. Primeiro, garante que o usuário está logado
        def decorator(*args, **kwargs):
            
            # 2. Pega o ID do usuário a partir do token
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            # 3. Verifica se o usuário é um admin
            if not user or user.role != 'admin':
                # Se não for, retorna um erro de 'Proibido'
                return jsonify({"message": "Acesso restrito a administradores"}), 403 
            
            # 4. Se for admin, permite que a rota original continue
            return fn(*args, **kwargs)
        return decorator
    return wrapper