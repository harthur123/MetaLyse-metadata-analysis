from src.extensions import db
from sqlalchemy.dialects.postgresql import JSON # ou from sqlalchemy import JSON
from datetime import datetime # Precisamos disso para o to_dict

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    filetype = db.Column(db.String(50))
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # <- Corrigido
    filehash = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    extracted_data = db.Column(db.JSON, nullable=True) 

    user = db.relationship('User', backref=db.backref('files', lazy=True))

    # --- ADICIONE ESTE MÉTODO ---
    def to_dict(self):
        """Converte o registro para um JSON que o frontend pode usar."""
        return {
            'id': self.id,
            'nome_arquivo': self.filename,
            'tipo_arquivo': self.filetype,
            'tamanho_bytes': self.filesize,
            'data_analise': self.upload_date.isoformat(),
            'hash': self.filehash,
            'usuario_responsavel': self.user.username, # <-- Pega o nome do usuário
            'metadados_extraidos': self.extracted_data
        }
    # --- FIM DA ADIÇÃO ---