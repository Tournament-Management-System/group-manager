import json
import sys 
from constants.DecimalEncoder import DecimalEncoder
from datetime import datetime as dt

class EventState():
    def __init__(self, info_list) -> None:
        self.id = info_list["id"]
        self.tournamentFormatId = info_list["tournamentFormatId"]
        self.eventFormatId = info_list["eventFormatId"]
        self.awards = info_list["awards"]
        self.currentRoundIdx = info_list["currentRoundIdx"]
        self.tournamentStateId = info_list["tournamentStateId"]
        self._version = info_list["_version"]
        self._deleted = info_list["_deleted"]
        self._lastChangedAt = info_list["_lastChangedAt"]
        self.createdAt = info_list["createdAt"]
        self.updatedAt = info_list["updatedAt"]
        
    def get_id(self):
        return self.id
    
    def get_tournamentFormatId(self):
        return self.tournamentFormatId
    
    def get_eventFormatId(self):
        return self.eventFormatId
    
    def get_awards(self):
        return self.awards
    
    def get_currentRoundIdx(self):
        return self.currentRoundIdx
    
    def get_tournamentStateId(self):
        return self.tournamentStateId
    
    def get_eventEventState_info(self):
        return {
            "id" : self.get_id(),
            "tournamentFormatId" : self.get_tournamentFormatId(),
            "eventFormatId": self.get_eventFormatId(),
            "awards" : self.get_awards(),
            "currentRoundIdx" : self.get_currentRoundIdx(),
            "tournamentStateId" : self.get_tournamentStateId(),
            "_version": self._version,
            "_deleted": self._deleted,
            "_lastChangedAt": self._lastChangedAt,
            "createdAt": self.createdAt,
            "updatedAt": dt.now().isoformat()
        }
    def get_eventInstance_json(self):
        return json.dumps(self.get_eventEventState_info)