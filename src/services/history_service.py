
from src.models.history import HistoryRecord

historico = []

def add_history(file_name, file_type, user):
    record = HistoryRecord(file_name, file_type, user)
    historico.append(record)
    return record.to_dict()

def get_all_history():
    return [h.to_dict() for h in historico]


    