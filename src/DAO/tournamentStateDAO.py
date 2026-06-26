from abc import ABC, abstractmethod

class tournamentStateDAO(ABC):
    @abstractmethod
    def getAllTournamentStates(self):
        pass
    @abstractmethod
    def getTournamentState(self, tournamentStateId):
        pass
    @abstractmethod
    def updateTournamentState(self, tournamentStateId, filed: dict):
        pass
    @abstractmethod
    def addTournamentState(self, tournamentStateId):
        pass
    @abstractmethod
    def deleteEventState(self, eventStateId):
        pass