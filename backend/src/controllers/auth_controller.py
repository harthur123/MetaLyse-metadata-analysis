
from flask import Blueprint, request, jsonify, current_app
from ..models.user import User
from .. import db
from ..extensions import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

# --- IMPORTAÇÃO CORRIGIDA ---
# Importa os validadores do novo local (utils)
from ..utils.validators import (
    validate_email_format, 
    validate_password_policy, 
    send_reset_email
)

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Tela de Cadastro: Cria um novo usuário."""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # --- VALIDAÇÃO MELHORADA ---
    if not username or not email or not password:
        return jsonify({"message": "Campos incompletos"}), 400

    if not validate_email_format(email):
        return jsonify({"message": "Formato de e-mail inválido"}), 400
        
    if not validate_password_policy(password):
        return jsonify({"message": "Senha fraca. Deve ter pelo menos 6 caracteres, maiúscula, minúscula, número e símbolo."}), 400
    # --- FIM DA VALIDAÇÃO ---

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email já cadastrado"}), 409
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username já cadastrado"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    
    # --- DEFININDO EMAIL DE ADMINISTRADOR ---
    if email.lower() == 'harthurhenrique214@gmail.com':
        new_user.role = 'admin'
        
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Tela de Login: Autentica o usuário e retorna tokens."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Campos incompletos"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Email ou senha inválidos"}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token,
        user_role=user.role 
    ), 200

@auth_bp.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    """Tela de Redefinição (Passo 1): Usuário pede o link."""
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    # --- LÓGICA DE EMAIL CORRIGIDA ---
    if user:
        send_reset_email(user) 
    # --- FIM DA LÓGICA DE EMAIL ---

    return jsonify({"message": "Se o email estiver cadastrado, um link será enviado."}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Tela de Redefinição (Passo 2): Usuário envia token e nova senha."""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    user = User.verify_reset_token(token)

    if not user:
        return jsonify({"message": "Token inválido ou expirado"}), 400

    # --- VALIDAÇÃO ---
    # Verifica se a NOVA senha também é forte
    if not validate_password_policy(new_password):
        return jsonify({"message": "Senha fraca. Deve ter pelo menos 6 caracteres, maiúscula, minúscula, número e símbolo."}), 400
    # --- FIM DA VALIDAÇÃO ---

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Senha atualizada com sucesso!"}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Rota protegida para o Angular buscar os dados do usuário logado."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
        
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200