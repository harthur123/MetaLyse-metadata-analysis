import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

# Importe os serviços que vamos usar
from ..services import metadata_service
from ..services import history_service

metadata_bp = Blueprint('metadata_bp', __name__)

# Configurações de upload
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@metadata_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    # --- 1. Validação do Arquivo ---
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "Nenhum arquivo selecionado"}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"message": "Tipo de arquivo não permitido (apenas PDF, JPG, JPEG)"}), 400

    # --- 2. Preparação para Salvar ---
    try:
        user_id = get_jwt_identity()
        filename = secure_filename(file.filename)
        
        # 'instance_path' é uma pasta segura fora do código 'src'
        upload_folder = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True) # Garante que a pasta exista
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # --- 3. Processamento do Arquivo ---
        file_type = filename.rsplit('.', 1)[1].lower()
        metadata = {}

        if file_type == 'pdf':
            metadata = metadata_service.extract_pdf_metadata(file_path)
        else: # jpg ou jpeg
            metadata = metadata_service.extract_image_metadata(file_path)

        # --- 4. Salvar no Histórico ---
        history_service.add_history(filename, file_type, user_id, status="Analisado")

        # --- 5. Retornar Sucesso ---
        return jsonify({
            "status": "success",
            "filename": filename,
            "metadata": metadata
        }), 200

    except Exception as e:
        current_app.logger.error(f"Falha no upload: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
    finally:
        # --- 6. Limpeza ---
        # Garante que o arquivo temporário seja deletado, mesmo se houver erro
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)