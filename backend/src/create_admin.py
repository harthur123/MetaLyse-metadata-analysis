from app import create_app, db # Ajuste o import conforme o nome da sua pasta principal
from app.models.user import User
from app.extensions import bcrypt

app = create_app()

with app.app_context():
    admin_email = 'harthurhenrique214@gmail.com'
    admin_pass = 'Mmtl_1511$aD5P'
    
    # Verifica se já existe
    user = User.query.filter_by(email=admin_email).first()
    
    if user:
        print("Usuário já existe. Atualizando para Admin...")
        user.role = 'admin'
        user.set_password(admin_pass) # Atualiza a senha para garantir
    else:
        print("Criando novo Admin...")
        new_admin = User(
            username='AdminMaster',
            email=admin_email,
            role='admin'
        )
        new_admin.set_password(admin_pass)
        db.session.add(new_admin)
    
    db.session.commit()
    print(f"Sucesso! Admin {admin_email} configurado.")