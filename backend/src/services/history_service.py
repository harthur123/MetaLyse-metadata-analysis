from ..extensions import db
from ..models.metadata import Metadata  # <--- IMPORTANDO A TABELA CORRETA
from ..models.user import User
from sqlalchemy import or_

class HistoryService:
    
    def get_history(self, user_id=None, search_term=None, is_admin=False):
        """
        Busca o histórico na tabela METADATA.
        """
        query = Metadata.query

        # 1. Lógica de Permissão
        if not is_admin:
            # SE FOR USUÁRIO COMUM:
            if user_id:
                # Convertemos para int() pois o token JWT pode trazer o ID como string
                query = query.filter(Metadata.user_id == int(user_id))
            else:
                return [] 
        # SE FOR ADMIN: Não filtra por ID, vê tudo.

        # 2. Lógica de Pesquisa (Barra de busca)
        if search_term:
            search = f"%{search_term}%"
            
            if is_admin:
                # Admin pode buscar por nome do arquivo OU nome do usuário
                query = query.join(User).filter(
                    or_(
                        Metadata.filename.ilike(search),
                        User.username.ilike(search),
                        User.email.ilike(search)
                    )
                )
            else:
                # Usuário comum só busca por nome do arquivo
                query = query.filter(Metadata.filename.ilike(search))

        # 3. Ordenação (Do mais novo para o mais antigo)
        # Usa upload_date se existir, senão ordena por ID
        if hasattr(Metadata, 'upload_date'):
            records = query.order_by(Metadata.upload_date.desc()).all()
        else:
            records = query.order_by(Metadata.id.desc()).all()
        
        # Retorna lista de dicionários usando o to_dict do modelo
        return [item.to_dict() for item in records]

    def get_by_id(self, metadata_id, user_id, is_admin=False):
        """Busca detalhes de um item específico."""
        record = Metadata.query.get(metadata_id)
        
        if not record:
            return None
            
        # Segurança: Se não for admin, só pode ver se o ID bater
        if not is_admin and record.user_id != int(user_id):
            return None
            
        return record.to_dict()