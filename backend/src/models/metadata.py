# Em: src/models/metadata.py

from src.extensions import db
from sqlalchemy.dialects.postgresql import JSON  # Importa o tipo JSON

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    filetype = db.Column(db.String(50))
    upload_date = db.Column(db.DateTime, nullable=False)
    filehash = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # --- AQUI ESTÁ A CORREÇÃO ---
    # Adiciona a coluna que faltava para armazenar o JSON 
    # dos metadados extraídos.
    extracted_data = db.Column(db.JSON, nullable=True) 
    # --- FIM DA CORREÇÃO ---

    user = db.relationship('User', backref=db.backref('files', lazy=True))