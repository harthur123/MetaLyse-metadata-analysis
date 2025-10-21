# src/controller/api.py (CORRIGIDO)

from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
# Removida a importação de 'check_password_hash' de werkzeug.security,
# pois bcrypt.check_password_hash já é usada no login_api.

# Importações dos módulos internos
from ..extensions import db, bcrypt
from ..models.User import User
from ..service.validators import validate_password_policy, validate_email_format, send_reset_email

# Novo Blueprint para API
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ---------------- Rotas de Autenticação ----------------

@api_bp.route("/register", methods=['POST'])
def register_api():
    # ... (código inalterado) ...
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados inválidos ou faltando."}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not validate_email_format(email):
        return jsonify({"message": "E-mail inválido."}), 400

    if not validate_password_policy(password):
        return jsonify({
            "message": "A senha deve ter pelo menos 6 caracteres, com maiúsculas, minúsculas, número e símbolo."
        }), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "Conta criada com sucesso!",
            "user_id": user.id
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Usuário ou e-mail já existentes."}), 409


@api_bp.route("/login", methods=['POST'])
def login_api():
    # ... (código inalterado) ...
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({
            "message": "Login realizado com sucesso!",
            "username": user.username
        }), 200
    else:
        return jsonify({"message": "Falha no login. Verifique suas credenciais."}), 401


# ---------------- Rotas de Sessão ----------------

@api_bp.route("/logout", methods=['POST'])
@login_required
def logout_api():
    logout_user()
    return jsonify({"message": "Você saiu da sua conta."}), 200


@api_bp.route("/user/status", methods=['GET'])
def user_status():
    if current_user.is_authenticated:
        return jsonify({
            "is_logged_in": True,
            "username": current_user.username,
            "user_id": current_user.id
        }), 200
    else:
        return jsonify({"is_logged_in": False}), 200


# ---------------- Rotas de Reset de Senha (Adaptadas) ----------------

@api_bp.route("/reset_request", methods=['POST'])
def reset_request_api():
    # ... (código inalterado) ...
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "E-mail não fornecido."}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        send_reset_email(user)

    return jsonify({
        "message": "Se o e-mail estiver cadastrado, enviamos instruções de redefinição."
    }), 200


# CORREÇÃO: Altera a URL da rota para '/reset_token/<token>'
@api_bp.route("/reset_token/<token>", methods=['POST'])
def reset_token_api(token):
    data = request.get_json()
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    user = User.verify_reset_token(token)

    if user is None:
        return jsonify({"message": "Link inválido ou expirado."}), 400

    if password != confirm_password:
        return jsonify({"message": "As senhas não coincidem."}), 400

    if not validate_password_policy(password):
        return jsonify({"message": "A nova senha não atende aos requisitos."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Senha atualizada com sucesso!"}), 200