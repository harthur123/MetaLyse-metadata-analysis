
from ..extensions import db, bcrypt 
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Este é o campo que armazena o hash
    password = db.Column(db.String(256), nullable=False) 
    
    role = db.Column(db.String(20), nullable=False, default='user')

    #histories = db.relationship("History", 
    #                            lazy=True, 
    #                           cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

    # --- Lógica de Senha (CORRIGIDA para usar BCRYPT e o campo 'password') ---
    
    def set_password(self, password):
        """Cria um hash seguro (com bcrypt) e salva no campo 'self.password'."""
        # Salva no campo 'password', não 'password_hash'
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verifica a senha (com bcrypt) lendo do campo 'self.password'."""
        # Lê do campo 'password'
        return bcrypt.check_password_hash(self.password, password)

    # --- Lógica de Redefinição de Senha --- (Já estava OK)
    
    def get_reset_token(self, expires_sec=1800):
        """Gera um token seguro para redefinição de senha (dura 30 min)."""
        s = Serializer(current_app.config['SECRET_KEY'], salt='password-reset-salt')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """Verifica o token de redefinição. Retorna o User se for válido."""
        s = Serializer(current_app.config['SECRET_KEY'], salt='password-reset-salt')
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data.get('user_id')
        except Exception:
            return None
        return User.query.get(user_id)