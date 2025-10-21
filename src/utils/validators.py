# src/service/validators.py (CORRIGIDO)
import re
# Importa url_for do Flask (não mais necessário importar o Message, pois já está no escopo)
from flask import url_for
from flask_mail import Message  # <--- Importamos Message para a função
from ..extensions import mail

# Regex para validação de senha (deve ter pelo menos 6 caracteres, maiúsculas, minúsculas, número e símbolo)
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=]).{6,}$'
# Regex para validação de e-mail
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def validate_password_policy(password):
    """Verifica se a senha atende à política de segurança."""
    return bool(re.fullmatch(PASSWORD_REGEX, password))


def validate_email_format(email):
    """Verifica se o e-mail tem um formato válido."""
    return bool(re.fullmatch(EMAIL_REGEX, email))


def send_reset_email(user):
    """Envia um e-mail com o link de redefinição de senha para o usuário."""
    # O user.get_reset_token() está definido na classe User (em src/models/User.py)
    token = user.get_reset_token()

    # Message() usa automaticamente as configurações de MAIL_DEFAULT_SENDER do app
    msg = Message('Redefinição de Senha', recipients=[user.email])

    # CORREÇÃO: Garante que o endpoint 'api.reset_token_api' seja usado
    msg.body = f'''Para redefinir sua senha, visite o seguinte link:
{url_for('api.reset_token_api', token=token, _external=True)}

Se você não solicitou isso, ignore este e-mail. O link expira em 30 minutos.
'''
    mail.send(msg)