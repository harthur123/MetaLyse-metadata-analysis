

from .. import db  
from ..models.history import History  
from ..models.User import User        

def add_history(file_name, file_type, user_id, status="Concluído"):
    
    user = User.query.get(user_id)
    if not user:
        raise Exception(f"Usuário com id {user_id} não encontrado para salvar o histórico")

    new_record = History(
        file_name=file_name,
        file_type=file_type,
        status=status,
        author=user  # Associa o objeto User completo!
    )

    db.session.add(new_record)
    db.session.commit()

    # 4. Retorna o novo registro como um dicionário
    return new_record.to_dict()


def get_all_history():
   
    records = History.query.order_by(History.created_at.desc()).all()
    
    # 2. Converte cada registro para um dicionário
    return [h.to_dict() for h in records]


def get_history_by_user_id(user_id):
   
    # 1. Verifica se o usuário existe
    user = User.query.get(user_id)
    if not user:
        return [] 
    
    # 2. Faz a query filtrando pelo user_id
    records = History.query.filter_by(user_id=user_id).order_by(History.created_at.desc()).all()
    
    # 3. Converte para dicionários
    return [h.to_dict() for h in records]