# run.py (Corrigido)

import os
from dotenv import load_dotenv

# 1. CARREGUE O .env ANTES DE QUALQUER IMPORTAÇÃO DA APLICAÇÃO
load_dotenv()

# --------------------------------------------------------

from src.__init__ import create_app # Agora, esta importação terá as variáveis

# Define o ambiente
CONFIG_NAME = os.environ.get('FLASK_CONFIG', 'default')

# Cria a aplicação
app = create_app(CONFIG_NAME)

if __name__ == '__main__':
    app.run()