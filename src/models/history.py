from .. import db
from datetime import datetime

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Concluído')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Chave Estrangeira que aponta para a tabela 'user'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relação que liga ao objeto User
    author = db.relationship('User', back_populates='histories')

    def __repr__(self):
        return f'<History {self.file_name}>'

    def to_dict(self):
        """Converte este objeto em um dicionário (JSON)."""
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
            'username': self.author.username
        }