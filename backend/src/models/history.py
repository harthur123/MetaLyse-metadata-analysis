from ..extensions import db
from datetime import datetime

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(10), nullable=False) # 'pdf', 'jpg', etc.
    filesize = db.Column(db.Integer, nullable=True) # Tamanho em bytes
    status = db.Column(db.String(50), nullable=False, default='Concluído')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Coluna mágica para guardar TODO o resultado da extração (JSON)
    extracted_data = db.Column(db.JSON, nullable=True)

    # Relacionamento com o Usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Backref cria uma propriedade virtual 'histories' no objeto User
    author = db.relationship("User", backref=db.backref('histories', lazy=True))

    def to_dict(self):
        """Converte para JSON para enviar ao Front."""
        return {
            'id': self.id,
            'filename': self.filename,
            'filetype': self.filetype,
            'filesize': self.filesize,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'author_name': self.author.username, # Para o Admin ver quem fez
            'author_email': self.author.email,
            'extracted_data': self.extracted_data # Os metadados reais
        }