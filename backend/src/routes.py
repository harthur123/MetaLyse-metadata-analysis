from flask import Blueprint, request, jsonify

# Cria um Blueprint para organizar rotas da API
api_bp = Blueprint('api', __name__)

# Rota de cadastro
@api_bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    # Aqui você pode salvar no banco ou apenas logar por enquanto
    print(f"Novo cadastro: {nome}, {email}")

    return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201

# Rota de status da API (útil para testes)
@api_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok'})
