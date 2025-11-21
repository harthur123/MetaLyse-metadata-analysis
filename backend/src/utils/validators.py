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
    Gera um token e envia um e-mail HTML (bonito) com um link 
    para o FRONTEND (Angular).
    """
    token = user.get_reset_token()
    
    # O link para o Angular (Frontend) está correto
    reset_link = f"http://localhost:4200/definir-senha?token={token}"


    # --- CORREÇÃO AQUI ---
    
    # 1. Crie o corpo em HTML (para o "Clique aqui")
    html_body = f"""
    <p>Olá {user.username},</p>
    <p>Para redefinir sua senha, por favor, clique no botão abaixo. O link é válido por 30 minutos.</p>
    <p style="margin-top: 20px; margin-bottom: 20px;">
        <a href="{reset_link}" 
           target="_blank"
           style="background-color: #007bff; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
           Clique Aqui para Redefinir sua Senha
        </a>
    </p>
    <p>Se você não fez esta solicitação, por favor, ignore este e-mail.</p>
    <p><small>Se o botão não funcionar, copie e cole este link no seu navegador: {reset_link}</small></p>
    """
    
    # 2. Crie o corpo em Texto Puro (como um fallback)
    text_body = f"""
    Olá {user.username},
    
    Para redefinir sua senha, copie e cole o seguinte link no seu navegador:
    {reset_link}

    Se você não fez esta solicitação, por favor, ignore este e-mail.
    O link expira em 30 minutos.
    """

    # 3. Crie a mensagem
    msg = Message(
        subject='[MetaLyse] Redefinição de Senha',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email]
    )
    
    # 4. Anexe os dois corpos (o cliente de e-mail escolherá qual usar)
    msg.body = text_body  # O fallback de texto
    msg.html = html_body  # O e-mail bonito em HTML

    try:
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Falha ao enviar e-mail de reset: {e}")
        raise e