from abc import ABC, abstractmethod

class roundStateDAO(ABC):
    @abstractmethod
    def getAllRoundStates(self):
        pass
    @abstractmethod
    def getRoundState(self, roundStateId):
        pass
    @abstractmethod
    def updateRoundState(self, roundStateId, filed: dict):
        pass
    @abstractmethod
    def addRoundState(self, roundStateId):
        pass
    