# Em: src/services/metadata_service.py

import os
import hashlib
from flask import current_app
from datetime import datetime
from PyPDF2 import PdfReader
from PIL import Image
import exiftool
from werkzeug.utils import secure_filename # Importação necessária

from src.extensions import db
from src.models.metadata import Metadata



class MetadataService:
    """Serviço responsável por processar, extrair e salvar metadados de arquivos."""

    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

    # 1. CORREÇÃO: Usa a pasta 'instance' para uploads, que é mais segura
    @property
    def UPLOAD_FOLDER(self):
        # current_app.instance_path aponta para a pasta 'instance' na raiz do backend
        folder = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(folder, exist_ok=True)
        return folder

    # ---------------------------
    # MÉTODO PRINCIPAL DE UPLOAD
    # ---------------------------
    def process_upload(self, file, user_id):
        """Salva o arquivo, extrai metadados, registra no banco E DELETA o arquivo."""
        
        if not file or not self._allowed_file(file.filename):
            raise ValueError("Tipo de arquivo não permitido")

        filepath = None # Define o 'filepath' fora do try
        
        try:
            # 1. SALVAR TEMPORARIAMENTE
            filename, filepath = self._save_file(file)
            
            # 2. ANALISAR O ARQUIVO
            file_hash = self._generate_hash(filepath)
            metadata_extracted = self._extract_metadata(filepath)

            # 3. SALVAR NO BANCO (SEM o filepath)
            metadata = Metadata(
                filename=filename,
                # filepath=filepath, # <-- REMOVIDO
                filesize=os.path.getsize(filepath),
                filetype=file.content_type,
                upload_date=datetime.utcnow(),
                filehash=file_hash,
                user_id=int(user_id),
                extracted_data=metadata_extracted
            )

            db.session.add(metadata)
            db.session.commit()

            return metadata, metadata_extracted
            
        finally:
            # 4. DELETAR O ARQUIVO (LÓGICA DE LIMPEZA)
            if filepath and os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    current_app.logger.info(f"Arquivo temporário deletado: {filepath}")
                except Exception as e:
                    current_app.logger.error(f"Falha ao deletar arquivo temporário: {e}")

    # ---------------------------
    # MÉTODOS AUXILIARES
    # ---------------------------
    def _allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def _save_file(self, file):
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.UPLOAD_FOLDER, filename)

        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(self.UPLOAD_FOLDER, filename)
            counter += 1

        file.save(filepath)
        return filename, filepath

    def _generate_hash(self, filepath):
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def _extract_metadata(self, filepath):
        """Determina o tipo e delega para o método específico."""
        ext = filepath.rsplit('.', 1)[-1].lower()
        if ext == 'pdf':
            return self._extract_pdf_metadata(filepath)
        elif ext in ('jpg', 'jpeg', 'png'):
            return self._extract_image_metadata(filepath)
        return {'info': 'Tipo suportado, mas sem extração detalhada.'}

    # ---------------------------
    # EXTRAÇÃO DE METADADOS
    # ---------------------------
    def _extract_pdf_metadata(self, file_path):
        """Extrai metadados de PDF (versão SEM 'Subject')."""
        metadata = {}
        try:
            reader = PdfReader(file_path)
            pdf_meta = reader.metadata
            metadata['page_count'] = str(len(reader.pages))
            
            if pdf_meta:
                def safe_get(key):
                    try:
                        value = pdf_meta.get(key, "")
                        return str(value) if value is not None else ""
                    except Exception as e:
                        current_app.logger.warning(f"Erro ao ler metadado {key}: {e}")
                        return ""
                
                metadata['title'] = safe_get('/Title')
                metadata['author'] = safe_get('/Author')
                metadata['creator'] = safe_get('/Creator')
                metadata['producer'] = safe_get('/Producer')
                
                # --- LINHAS ADICIONADAS AQUI ---
                # Padroniza os nomes para corresponder ao que o ExifTool retorna
                metadata['FileCreateDate'] = safe_get('/CreationDate')
                metadata['FileModifyDate'] = safe_get('/ModDate')
                # --- FIM DA ADIÇÃO ---

            metadata = {
                k: v for k, v in metadata.items()
                if v and v.strip().lower() != "none"
            }
        except Exception as e:
            current_app.logger.error(f"Erro ao ler PDF '{file_path}': {e}")
        return metadata

    def _extract_image_metadata(self, file_path):
        """Extrai metadados de Imagem (com ExifToolHelper)."""
        metadata = {}
        try:
            with Image.open(file_path) as img:
                metadata['width'] = img.width
                metadata['height'] = img.height
                metadata['format'] = img.format
                exif_data = img.getexif()
                if exif_data:
                    metadata['pillow_exif_items'] = len(exif_data)
        except Exception as e:
            current_app.logger.warning(f"Erro Pillow: {e}")

        try:
            # Caminho para 'backend/exiftool/exiftool.exe'
            exe_path = os.path.join(current_app.root_path, '..', 'exiftool', 'exiftool.exe')
            
            if not os.path.exists(exe_path):
                raise FileNotFoundError("exiftool.exe não encontrado em backend/exiftool/")
            
            with exiftool.ExifToolHelper(executable=exe_path) as et:
                exif_metadata_list = et.get_metadata(file_path)
                exif_metadata = exif_metadata_list[0]
            
            cleaned = {k.split(':')[-1]: v for k, v in exif_metadata.items()}
            metadata['exiftool_data'] = cleaned
        
        except Exception as e:
            current_app.logger.warning(f"Erro ExifTool: {e}")

        return metadata