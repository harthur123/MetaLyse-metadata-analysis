from ..extensions import db
from ..models.metadata import Metadata # <-- Importa o modelo Metadata
from ..models.user import User
from sqlalchemy import or_

class HistoryService:
    
    def get_history(self, user_id=None, search_term=None, is_admin=False):
        """
        Busca o histórico.
        - Se user_id for passado: Retorna apenas daquele usuário (Visão Usuário).
        - Se is_admin=True: Retorna de TODOS (Visão Admin).
        - search_term: Filtra por nome do arquivo, tipo ou nome do autor (se admin).
        """
        
        # Começa a query na tabela Metadata
        query = Metadata.query

        # 1. Filtro de Permissão (Usuário vs Admin)
        if not is_admin:
            if user_id:
                query = query.filter_by(user_id=user_id)
            else:
                return [] # Sem ID e sem admin = nada

        # 2. Filtro de Pesquisa (Search Bar)
        if search_term:
            search = f"%{search_term}%" # % serve para buscar partes do texto
            
            if is_admin:
                # Admin pode buscar por Nome do Arquivo OU Nome do Autor
                query = query.join(User).filter(
                    or_(
                        Metadata.filename.ilike(search),
                        User.username.ilike(search),
                        User.email.ilike(search)
                    )
                )
            else:
                # Usuário comum busca apenas nos seus arquivos
                query = query.filter(Metadata.filename.ilike(search))

        # 3. Ordenação (Mais recente primeiro)
        records = query.order_by(Metadata.upload_date.desc()).all()
        
        return [h.to_dict() for h in records] # <-- Usa o método to_dict()

    def get_by_id(self, metadata_id, user_id, is_admin=False):
        """Busca um registro específico para detalhes/exportação."""
        record = Metadata.query.get(metadata_id)
        
        if not record:
            return None
            
        # Segurança: Se não for admin, só pode ver o próprio registro
        if not is_admin and record.user_id != user_id:
            return None
            
        return record.to_dict()