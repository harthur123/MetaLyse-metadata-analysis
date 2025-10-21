# Em: src/models/User.py

from ..extensions import db  # Usando o 'extensions' (do parceiro, que é uma boa prática)
from werkzeug.security import generate_password_hash, check_password_hash # (do seu HEAD)
from itsdangerous import URLSafeTimedSerializer as Serializer # (do seu HEAD)
from flask import current_app # (de ambos)
from flask_login import UserMixin # (do parceiro)

class User(db.Model, UserMixin): # <--- COMBINADO
    __tablename__ = 'user' # (do seu HEAD)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # (do seu HEAD, 80 é > 20)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # (do seu HEAD)
    
    # --- CAMPO CHAVE PARA ADMIN vs USER --- (do seu HEAD)
    role = db.Column(db.String(20), nullable=False, default='user') # 'user' ou 'admin'

    # --- Relacionamento com History --- (do seu HEAD)
    histories = db.relationship('History', 
                                  back_populates='author', 
                                  lazy=True, 
                                  cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

    # --- Lógica de Senha --- (do seu HEAD)
    def set_password(self, password):
        """Cria um hash seguro para a senha."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida bate com o hash."""
        return check_password_hash(self.password_hash, password)

    # --- Lógica de Redefinição de Senha --- (COMBINADA)
    
    # (do seu HEAD - bom pois usa 'salt')
    def get_reset_token(self, expires_sec=1800):
        """Gera um token seguro para redefinição de senha (dura 30 min)."""
        s = Serializer(current_app.config['SECRET_KEY'], salt='password-reset-salt')
        return s.dumps({'user_id': self.id})

    @staticmethod
    # (do parceiro - bom pois retorna User/None, mas corrigido para usar o 'salt')
    def verify_reset_token(token, expires_sec=1800):
        """Verifica o token de redefinição. Retorna o User se for válido."""
        s = Serializer(current_app.config['SECRET_KEY'], salt='password-reset-salt') # <--- CORRIGIDO
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data.get('user_id')
        except Exception:
            return None
        return User.query.get(user_id)