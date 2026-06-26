from abc import ABC, abstractmethod

class GroupDAO(ABC):
    @abstractmethod
    def getAllGroups(self):
        pass
    @abstractmethod
    def getGroup(self, groupId):
        pass
    @abstractmethod
    def updateGroup(self, groupId, filed: dict):
        pass
    @abstractmethod
    def deleteGroup(self, groupId):
        pass
    @abstractmethod
    def addGroup(self, group):
        pass
    @abstractmethod
    def getGroupsbyRoundId(self, roundId):
        pass