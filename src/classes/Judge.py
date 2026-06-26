from User import User

class Judge(User):
    def __init__(self, jid = '', isAssigned = False):
        self.jid = jid
        self.assigned = isAssigned

    def getJudgeInfo(self):
        returnDict = self.get_user_info()
        returnDict['judgeId'] = self.jid
        returnDict['assigned'] = self.assigned
        return returnDict