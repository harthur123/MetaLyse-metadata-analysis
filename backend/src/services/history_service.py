from ..extensions import db
from ..models.history import History
from ..models.user import User
from sqlalchemy import or_

class HistoryService:
    
    def create_entry(self, filename, filetype, filesize, user_id, metadata_json):
        """Cria um novo registro no histórico."""
        new_record = History(
            filename=filename,
            filetype=filetype,
            filesize=filesize,
            user_id=user_id,
            extracted_data=metadata_json,
            status="Concluído"
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record

    def get_history(self, user_id=None, search_term=None, is_admin=False):
        """
        Busca o histórico.
        - Se user_id for passado: Retorna apenas daquele usuário (Visão Usuário).
        - Se is_admin=True: Retorna de TODOS (Visão Admin).
        - search_term: Filtra por nome do arquivo, tipo ou nome do autor (se admin).
        """
        query = History.query

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
                        History.filename.ilike(search),
                        User.username.ilike(search),
                        User.email.ilike(search)
                    )
                )
            else:
                # Usuário comum busca apenas nos seus arquivos
                query = query.filter(History.filename.ilike(search))

        # 3. Ordenação (Mais recente primeiro)
        records = query.order_by(History.created_at.desc()).all()
        
        return [h.to_dict() for h in records]

    def get_by_id(self, history_id, user_id, is_admin=False):
        """Busca um registro específico para detalhes/exportação."""
        record = History.query.get(history_id)
        
        if not record:
            return None
            
        # Segurança: Se não for admin, só pode ver o próprio registro
        if not is_admin and record.user_id != user_id:
            return None
            
        return record.to_dict()