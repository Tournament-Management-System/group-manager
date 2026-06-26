from abc import ABC, abstractmethod

class eventStateDAO(ABC):
    @abstractmethod
    def getAllEventState(self):
        pass
    @abstractmethod
    def getEventState(self, eventStateId):
        pass
    @abstractmethod
    def updateEventState(self, eventStateId, filed: dict):
        pass
    @abstractmethod
    def deleteEventState(self, eventStateId):
        pass
    @abstractmethod
    def addEventState(self, eventState):
        pass
    