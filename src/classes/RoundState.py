import json
import sys 
from datetime import datetime as dt
from constants.DecimalEncoder import DecimalEncoder

class RoundState:
    def __init__(self, info_list) -> None:
        self.id = info_list["id"]
        self.tournamentFormatId = info_list["tournamentFormatId"]
        self.tournamentStateId = info_list["tournamentStateId"]
        self.eventFormatId = info_list["eventFormatId"]
        self.eventStateId = info_list["eventStateId"]
        self.queued = info_list["queued"]
        self.assigned = info_list["assigned"]
        self.completed = info_list["completed"]
        self.started = info_list["started"]
        self._version = info_list["_version"]
        self._deleted = info_list["_deleted"]
        self._lastChangedAt = info_list["_lastChangedAt"]
        self.createdAt = info_list["createdAt"]
        self.updatedAt = info_list["updatedAt"]
    def get_id(self):
        return self.id
    
    def get_queued(self):
        return self.queued
    
    def get_assigned(self):
        return self.assigned
    
    def get_started(self):
        return self.started
    
    def get_completed(self):
        return self.completed
    
    def get_tournamentFormatId(self):
        return self.tournamentFormatId
    
    def get_tournamentStateId(self):
        return self.tournamentStateId
    
    def get_eventFormatId(self):
        return self.eventFormatId
    
    def get_eventStateId(self):
        return self.eventStateId
    
    def queued_to_assigned(self, group):
        for g in self.queued:
            g_parse = json.loads(g)
            group_parse = json.loads(group)
            if g_parse["groupId"] == group_parse["groupId"]:
                self.queued.remove(g)
                self.assigned.append(group)
                break
        
    def assigned_to_started(self, group):
        for g in self.assigned:
            g_parse = json.loads(g)
            group_parse = json.loads(group)
            if g_parse["groupId"] == group_parse["groupId"]:
                self.assigned.remove(g)
                self.started.append(group)
                break
        

    def started_to_completed(self, group):
        for g in self.started:
            g_parse = json.loads(g)
            group_parse = json.loads(group)
            if g_parse["groupId"] == group_parse["groupId"]:
                self.started.remove(g)
                self.completed.append(group)
                break
    
    def update_version(self):
        self._version += 1
        
    def all_completed(self):
        return len(self.queued) == 0 and len(self.assigned) == 0 and len(self.started) == 0
        
    def get_round_info(self):
        return {
            "roundStateId" : self.get_id(),
            "queued" : self.get_queued(),
            "assigned" : self.get_assigned(),
            "completed": self.get_completed(),
            "started": self.get_started(),
            "tournamentFormatId": self.get_tournamentFormatId(),
            "tournamentStateId": self.get_tournamentStateId(),
            "eventFormatId": self.get_eventFormatId(),
            "eventStateId": self.get_eventStateId(),
            "_version": self._version,
            "_deleted": self._deleted,
            "_lastChangedAt": self._lastChangedAt,
            "createdAt": self.createdAt,
            "updatedAt": dt.now().isoformat()
        }  
    
    def get_round_json(self):
        return json.dumps(
            self.get_round_info()
        )  