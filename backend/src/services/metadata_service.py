
import os
from flask import current_app
from PyPDF2 import PdfReader
from PIL import Image  # Pillow
import exiftool

def extract_pdf_metadata(file_path):
    """Extrai metadados de um arquivo PDF."""
    metadata = {}
    try:
        reader = PdfReader(file_path)
        pdf_meta = reader.metadata
        
        metadata['page_count'] = len(reader.pages)
        if pdf_meta:
            metadata['title'] = pdf_meta.title
            metadata['author'] = pdf_meta.author
            metadata['subject'] = pdf_meta.subject
            metadata['creator'] = pdf_meta.creator
            metadata['producer'] = pdf_meta.producer
            
            # Limpa valores None
            metadata = {k: v for k, v in metadata.items() if v is not None}

        return metadata
    
    except Exception as e:
        current_app.logger.error(f"Erro ao ler PDF: {e}")
        raise ValueError(f"Não foi possível processar o PDF: {e}")

def extract_image_metadata(file_path):
    """Extrai metadados de um arquivo JPG/JPEG."""
    metadata = {}
    
    # --- 1. Extração com Pillow (Básico e Rápido) ---
    try:
        with Image.open(file_path) as img:
            metadata['image_width'] = img.width
            metadata['image_height'] = img.height
            metadata['image_format'] = img.format
            
            # Tenta pegar o EXIF básico do Pillow
            exif_data = img.getexif()
            if exif_data:
                metadata['pillow_exif_items'] = len(exif_data)

    except Exception as e:
        current_app.logger.error(f"Erro com Pillow: {e}")
        # Não levanta erro, pois o ExifTool ainda pode funcionar

    # --- 2. Extração com PyExifTool (Completo) ---
    try:
        # current_app.root_path é a pasta 'src'. .. sobe um nível.
        executable_path = os.path.join(current_app.root_path, '..', 'exiftool.exe')

        if not os.path.exists(executable_path):
            raise FileNotFoundError("exiftool.exe não encontrado na raiz do backend.")

        with exiftool.ExifTool(executable=executable_path) as et:
            exif_metadata = et.get_metadata(file_path)
        
        # O ExifTool retorna MUITA coisa. Vamos filtrar e limpar.
        cleaned_exif = {}
        for k, v in exif_metadata.items():
            # Remove chaves de grupo (ex: 'EXIF:', 'File:') e deixa só o nome
            key_name = k.split(':')[-1]
            cleaned_exif[key_name] = v
            
        metadata['exiftool_data'] = cleaned_exif

    except Exception as e:
        current_app.logger.error(f"Erro com ExifTool: {e}")
        # Se o Pillow funcionou, podemos retornar pelo menos isso.
        if not metadata:
             raise ValueError(f"Não foi possível processar a imagem: {e}")

    return metadata