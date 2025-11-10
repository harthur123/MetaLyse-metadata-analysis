# Em: src/utils/validators.py
import re
from flask import current_app
from flask_mail import Message
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
    """
    Gera um token e envia um e-mail com um link para o FRONTEND (Angular).
    """
    # O user.get_reset_token() está definido na classe User (em src/models/User.py)
    token = user.get_reset_token()

    # --- AQUI ESTÁ A LÓGICA CORRETA ---
    # O link que enviamos no e-mail deve apontar para o seu
    # aplicativo Angular, que estará rodando em localhost:4200.
    reset_link = f"http://localhost:4200/reset-password?token={token}"

    # Cria a mensagem de e-mail
    msg = Message(
        subject='[MetaLyse] Redefinição de Senha',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        body=f'''Para redefinir sua senha, visite o seguinte link:
{reset_link}

Se você não fez esta solicitação, por favor, ignore este e-mail.
'''
    )
    
    # Tenta enviar o e-mail
    try:
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Falha ao enviar e-mail de reset: {e}")
        # Se falhar, nós (por enquanto) não quebramos o app, 
        # mas logamos o erro no terminal.