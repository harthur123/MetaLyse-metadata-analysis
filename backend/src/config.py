# src/config.py
import os


# Certifica-se de que o .env foi carregado no run.py
# Aqui apenas referenciamos as variáveis de ambiente
class Config:
    # Chave Secreta
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY não foi configurada! Verifique seu arquivo .env.")

    # Configurações do Banco de Dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Boa prática para evitar warnings

    # Configurações do Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))

    # Converte o valor de string ('True' ou 'False') para booleano
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 't', '1']

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = str(os.environ.get('MAIL_PASSWORD'))
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    
    JWT_BLOCKLIST_ENABLED = True
    JWT_BLOCKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # ... outras configs ...
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Aqui você poderia ter um banco de dados diferente para produção
    # SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL')


# Mapeamento para uso no __init__.py
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}