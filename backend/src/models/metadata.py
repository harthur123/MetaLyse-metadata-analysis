from ..extensions import db
from datetime import datetime
from ..models.user import User # Importante para o Admin ver o nome

class Metadata(db.Model):
    __tablename__ = 'metadata' # Nome da tabela onde o upload salva

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    
    # Padroniza o tipo de arquivo
    filetype = db.Column(db.String(50), nullable=False)
    filesize = db.Column(db.Integer, nullable=True)
    
    # O MetadataService salva 'upload_date', usamos ele como padrão
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    filehash = db.Column(db.String(128), nullable=True)

    # Aqui ficam os dados JSON da análise
    extracted_data = db.Column(db.JSON, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relacionamento para pegar nome e email do autor
    user = db.relationship('User', backref=db.backref('metadatas', lazy=True))

    def to_dict(self):
        """Retorna os dados para o Angular."""
        return {
            'id': self.id,
            'filename': self.filename,
            'filetype': self.filetype,
            'filesize': self.filesize,
            # O Angular espera uma data. Enviamos upload_date formatada.
            'created_at': self.upload_date.isoformat() if self.upload_date else datetime.utcnow().isoformat(),
            
            'extracted_data': self.extracted_data,

            # Dados extras para o Admin
            'author_name': self.user.username if self.user else 'Desconhecido',
            'author_email': self.user.email if self.user else 'N/A'
        }