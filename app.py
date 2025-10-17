import os
import re
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

# ----------------- 1. Inicialização e Configuração -----------------

load_dotenv()

app = Flask(__name__)

# Configurações de Aplicativo
secret_key_value = os.environ.get('SECRET_KEY')

if secret_key_value is None:
    raise ValueError("SECRET_KEY não foi configurada! Verifique seu arquivo .env.")

app.config['SECRET_KEY'] = secret_key_value
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 't', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = str(os.environ.get('MAIL_PASSWORD'))
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# ----------------- 2. Modelo de Dados -----------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    # Geração do token seguro
    def get_reset_token(self):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    # Verificação do token
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------- 2.1. Validações -----------------

PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=]).{6,}$'
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def validate_password_policy(password):
    return bool(re.fullmatch(PASSWORD_REGEX, password))


def validate_email_format(email):
    return bool(re.fullmatch(EMAIL_REGEX, email))


# ----------------- 3. Função de Envio de E-mail -----------------

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Redefinição de Senha', recipients=[user.email])
    msg.body = f'''Para redefinir sua senha, visite o seguinte link:
{url_for('reset_token', token=token, _external=True)}

Se você não solicitou isso, ignore este e-mail. O link expira em 30 minutos.
'''
    mail.send(msg)


# ----------------- 4. Rotas -----------------

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not validate_email_format(email):
            flash('E-mail inválido.', 'danger')
            return render_template('register.html')

        if not validate_password_policy(password):
            flash('A senha deve ter pelo menos 6 caracteres, com letras maiúsculas, minúsculas, número e símbolo.', 'danger')
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Usuário ou e-mail já existentes.', 'danger')

    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Falha no login. Verifique suas credenciais.', 'danger')

    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))


@app.route("/home")
@login_required
def home():
    return f"Olá, {current_user.username}! Bem-vindo à página protegida."


# ----------------- 5. Reset de Senha -----------------

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not validate_email_format(email):
            flash('E-mail inválido.', 'danger')
            return render_template('reset_request.html')

        if user:
            send_reset_email(user)
        flash('Se o e-mail estiver cadastrado, enviamos instruções de redefinição.', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html')


@app.route("/reset_token/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('Link inválido ou expirado.', 'warning')
        return redirect(url_for('reset_request'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('reset_token.html', token=token)

        if not validate_password_policy(password):
            flash('A nova senha não atende aos requisitos.', 'danger')
            return render_template('reset_token.html', token=token)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Senha atualizada com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', token=token)


# ----------------- 6. Execução -----------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
