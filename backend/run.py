# Em: backend/run.py

import os
import sys
from dotenv import load_dotenv

# --- CORREÇÃO DO PATH ---
# Adiciona a pasta 'backend' (onde este arquivo está) ao path do Python
# Isso conserta todos os erros de importação 'src.models.User'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# ------------------------

# Carregue o .env ANTES de QUALQUER IMPORTAÇÃO DA APLICAÇÃO
load_dotenv()

from src import create_app

# Define o ambiente
CONFIG_NAME = os.environ.get('FLASK_CONFIG', 'default')

# Cria a aplicação
app = create_app(CONFIG_NAME)

if __name__ == '__main__':
    # Você pode querer definir a porta no seu .env também
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)