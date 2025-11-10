import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

# --- CORREÇÃO DE IMPORTAÇÃO ---
# Importa as funções específicas do nosso serviço de metadados unificado
from ..services.metadata_service import extract_pdf_metadata, extract_image_metadata

metadata_bp = Blueprint('metadata_bp', __name__)

# Configurações de upload
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@metadata_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():

    # --- NOSSO TESTE DE DEBATE ---
    # Se o Postman mostrar esta mensagem, o código está ATUALIZADO.
    return jsonify({"message": "TESTE - O CÓDIGO NOVO ESTÁ RODANDO"}), 418
    # --- FIM DO TESTE ---

    # O resto do seu código (que não será executado por enquanto):
    
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
        
        upload_folder = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # --- 3. Processamento do Arquivo (COM LÓGICA CORRIGIDA) ---
        file_type = filename.rsplit('.', 1)[1].lower()
        metadata = {}

        if file_type == 'pdf':
            metadata = metadata_service.extract_pdf_metadata(file_path)
        else: # jpg ou jpeg
            metadata = extract_image_metadata(file_path) # <-- Corrigido para chamar sua função detalhada

        
        # --- 4. Salvar no Histórico (Continua desativado, como pedimos) ---
        
        # history_service.add_history(
        #     filename=filename, 
        #     file_type=file_type, 
        #     user_id=user_id, 
        #     status="Analisado",
        #     metadata=metadata
        # )
        
        # --- FIM DA MODIFICAÇÃO ---
        
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
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)