import os

# Pega o caminho absoluto da pasta onde este arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Chave secreta para JWT e tokens de reset
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha-chave-secreta-muito-dificil'
    
    # Configuração do Banco de Dados (vamos usar SQLite para ser fácil de testar)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'meu-jwt-secreto-tambem'