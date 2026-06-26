import json
import sys 
from constants.DecimalEncoder import DecimalEncoder
class Group():
    def __init__(self, info_list) -> None:
        self.id = info_list["groupId"]
        self.roomId = info_list["roomId"]
        self.judges = info_list["judges"]
        self.competitors = info_list["competitors"]
        self.ranking = info_list["ranking"]
        self.comments = info_list["comments"]
        
    def get_id(self):
        return self.id
    
    def get_roomId(self):
        return self.roomId
    
    def get_judges(self):
        return self.judges
    
    def get_competitors(self):
        return self.competitors
    
    def get_ranking(self):
        return self.ranking
    
    def get_comments(self):
        return self.comments
    
    def set_roomId(self, newRoomId):
        self.roomId = newRoomId
        
    def set_judges(self, newJudegesId):
        self.judges = newJudegesId
        
    def set_ranking(self, newRanking):
        self.ranking = newRanking
    
    def set_competitors(self, newCompetitorId):
        self.competitors = newCompetitorId
    
    def set_comments(self, newComments):
        self.comments = newComments
        
    def get_group_info(self):
        return {
            "groupId" : self.get_id(),
            "roomId": self.get_roomId(),
            "judges": self.get_judges(),
            "competitors": self.get_competitors(),
            "ranking" : self.get_ranking(),
            "comments": self.get_comments(),
        }
    
    def get_group_json(self):
        return json.dumps(self.get_group_info())