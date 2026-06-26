import json
import sys 
from constants.DecimalEncoder import DecimalEncoder
from datetime import datetime as dt

class EventFormat():
    def __init__(self, info_list) -> None:
        self.id = info_list["id"]
        self.awards = info_list["awards"]
        self.rounds = info_list["rounds"]
        self.name = info_list["name"]
        self.owner = info_list["owner"]
        self._version = info_list["_version"]
        self._deleted = info_list["_deleted"]
        self._lastChangedAt = info_list["_lastChangedAt"]
        self.updatedAt = info_list["updatedAt"]
        self.createdAt = info_list["createdAt"]
    def get_id(self):
        return self.id
    
    def get_awards(self):
        return self.awards
    
    def get_rounds(self):
        return self.rounds
    
    def get_name(self):
        return self.name
    
    def get_owner(self):
        return self.owner
    
    def get_event_info(self):
        return {
            "id" : self.get_id(),
            "awards" : self.get_awards(),
            "name": self.get_name(),
            "owner": self.get_owner(),
            "rounds" : self.get_rounds(),
            "_version": self._version,
            "_deleted": self._deleted,
            "createdAt": self.createdAt,
            "_lastChangedAt": self._lastChangedAt,
            "updatedAt": dt.now().isoformat()
        }
    def get_event_json(self):
        return json.dumps(self.get_event_info)