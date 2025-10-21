# src/models/User.py (CORRIGIDO)
from itsdangerous import URLSafeTimedSerializer
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError
from flask import current_app # <--- NOVA IMPORTAÇÃO
from ..extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    # Geração do token seguro
    def get_reset_token(self):
        # CORREÇÃO: Usa current_app para obter a chave secreta
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    # Verificação do token
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        # CORREÇÃO: Usa current_app para obter a chave secreta
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)