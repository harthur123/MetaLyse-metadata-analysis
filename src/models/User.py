# Em: src/models/User.py

from .. import db # Importa a instância 'db' do 'src/__init__.py'
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # --- CAMPO CHAVE PARA ADMIN vs USER ---
    role = db.Column(db.String(20), nullable=False, default='user') # 'user' ou 'admin'

    # --- Relacionamento com History ---
    # Um usuário tem muitos históricos. 'back_populates' liga com o 'author' no History.
    # 'cascade' significa que se o usuário for deletado, seu histórico vai junto.
    histories = db.relationship('History', 
                                back_populates='author', 
                                lazy=True, 
                                cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

    # --- Lógica de Senha ---
    def set_password(self, password):
        """Cria um hash seguro para a senha."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida bate com o hash."""
        return check_password_hash(self.password_hash, password)

    # --- Lógica de Redefinição de Senha ---
    def get_reset_token(self, expires_sec=1800):
        """Gera um token seguro para redefinição de senha (dura 30 min)."""
        s = Serializer(current_app.config['SECRET_KEY'], salt='password-reset-salt')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        """Verifica o token de redefinição. Retorna o User se for válido."""
        s = Serializer(current_app.config['SECRET_KEY'], salt='password-reset-salt')
        try:
            data = s.loads(token, max_age=1800)
            user_id = data.get('user_id')
        except:
            return None
        return User.query.get(user_id)