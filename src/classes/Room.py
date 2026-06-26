from Judge import Judge
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Room():
    def __init__(self, roomId = '', eventId = '', status = '', competitors = [], judge = Judge()):
        self.roomId = roomId
        self.eventId = eventId
        self.status = status
        self.competitors = competitors
        self.judge = judge

    def checkJid(self, jid: str):
        if (jid != self.judge.jid):
            return False
        return True
    
    def getRoomInfo(self):
        return {
            'roomId': self.roomId,
            'eventId': self.eventId,
            'status': self.status,
            'competitors': self.competitors,
            'judge': self.judge,
        }
