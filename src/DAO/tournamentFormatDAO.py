from abc import ABC, abstractmethod

class tournamentFormatDAO(ABC):
    @abstractmethod
    def getAllTournamentFormat(self):
        pass
    @abstractmethod
    def getTournamentFormat(self, tournamentFormatId):
        pass
    @abstractmethod
    def updateTournamentFormat(self, tournamentFormatId, filed: dict):
        pass
    @abstractmethod
    def deleteTournamentFormat(self, tournamentFormatId):
        pass
    @abstractmethod
    def addTournamentFormat(self, tournament):
        pass
    