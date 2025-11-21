from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.metadata_service import MetadataService

metadata_bp = Blueprint('metadata', __name__, url_prefix='/api/metadata')
service = MetadataService()

@metadata_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_metadata():
    user_id = get_jwt_identity()
    file = request.files.get('file')

    if not file:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    try:
        metadata, metadata_extracted = service.process_upload(file, user_id)
        return jsonify({
            'message': 'Upload e extração concluídos com sucesso!',
            'file': {
                'nome': metadata.filename,
                'tipo': metadata.filetype,
                'tamanho_bytes': metadata.filesize,
                'hash': metadata.filehash
            },
            'metadados_extraidos': metadata_extracted
        }), 201
    except ValueError as e:
        # Mensagem amigável para arquivo duplicado
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao processar o arquivo.'}), 500
