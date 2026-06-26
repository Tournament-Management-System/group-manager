from User import User

class TournamentState():

    def __init__(self, tournamentId = '', events = [], competitors = [], judges = [], rooms = [], status = 'INACTIVE'):
        self.tournamentId = tournamentId
        self.events = events
        self.competitors = competitors
        self.judges = judges
        self.rooms = rooms
        self.status = status

    def checkAdmin(self, uid: str):
        # get user from dyanmodb
        User('uid', ['Admin', 'User'])
        return User.isUserAdmin()

    def getTournamentInfo(self):
        return {
            'tournamentId': self.tournamentId,
            'events': self.events,
            'competitors': self.competitors,
            'judges': self.judges,
            'rooms': self.rooms,
            'status': self.status,
        }

class TournamentFormat():
    def __init__(self):
        self.formatId = ''
        self.name = ''
        self.description = ''
        self.startTime = ''
        self.eventFee = 0.00
        self.venueId = ''
        self.judges = []
        self.competitorEntryIds = []

    def getTournamentFormatInfo(self):
        return {
            'formatId': self.formatId,
            'name': self.name,
            'description': self.description,
            'startTime': self.startTime,
            'eventFee': self.eventFee,
            'venueId': self.venueId,
            'judges': self.judges,
            'competitorEntryIds': self.competitorEntryIds,
        }