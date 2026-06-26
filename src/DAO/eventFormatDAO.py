from abc import ABC, abstractmethod

class eventFormatDAO(ABC):
    @abstractmethod
    def getAllEventFormat(self):
        pass
    @abstractmethod
    def getEventFormat(self, eventFormatId):
        pass
    @abstractmethod
    def updateEventFormat(self, eventFormatId, filed: dict):
        pass
    @abstractmethod
    def deleteEventFormat(self, eventFormatId):
        pass
    @abstractmethod
    def addEventFormat(self, event):
        pass
    