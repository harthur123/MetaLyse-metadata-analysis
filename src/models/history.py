
import datetime

class HistoryRecord:
    def _init_(self, file_name, file_type, user, status="Concluído"):
        self.file_name = file_name
        self.file_type = file_type
        self.user = user
        self.status = status
        self.date = datetime.dateTime.now().strftime("%d/%m/%Y %H:%M")


    def to_dict(self):
        return {
            "file_name": self.file_name,
            "file_type": self.file_type,
            "user": self.user,
            "status": self.status,
            "date": self.date
        }