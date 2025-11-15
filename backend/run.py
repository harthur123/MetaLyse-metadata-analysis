import os
from dotenv import load_dotenv

# 1. CARREGUE O .env ANTES DE TUDO
# Isso garante que a SECRET_KEY e o DB_URI estejam disponíveis
load_dotenv()

# 2. Importe o create_app (APENAS UMA VEZ)
from src import create_app
# Importe as extensões e modelos que o comando 'seed' vai precisar
from src.extensions import db, bcrypt
from src.models.user import User

# 3. Define o ambiente e cria o app
config_name = os.environ.get('FLASK_CONFIG', 'default')
app = create_app(config_name)

# 4. Define o comando CLI
@app.cli.command("seed-admin")
def seed_admin():
    """Cria a conta de administrador padrão a partir do .env"""
    
    # 5. Adiciona o CONTEXTO DO APP (MUITO IMPORTANTE!)
    # Isso permite que o comando acesse o banco de dados
    with app.app_context():
        print("Iniciando o 'seed' do administrador...")
        
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_pass = os.environ.get('ADMIN_PASSWORD')
        
        if not admin_email or not admin_pass:
            print("Erro: ADMIN_EMAIL e ADMIN_PASSWORD não configurados no .env")
            return

        # Procura se o admin já existe
        user = User.query.filter_by(email=admin_email).first()
        
        if not user:
            # Se não existe, cria
            hashed_password = bcrypt.generate_password_hash(admin_pass).decode('utf-8')
            new_admin = User(
                email=admin_email,
                password=hashed_password,
                username="Admin (Harthur)", 
                role="admin"
            )
            db.session.add(new_admin)
            db.session.commit()
            print(f"Administrador '{admin_email}' criado com sucesso.")
        else:
            # Se já existe
            print(f"Administrador '{admin_email}' já existe.")
# --- FIM DO COMANDO ---

# 6. Roda o servidor
if __name__ == '__main__':
    app.run(debug=True)