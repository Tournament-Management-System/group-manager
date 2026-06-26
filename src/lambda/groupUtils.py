import os
from aws_helper.AppSyncQuery import AppSync_query

class groupUtils():
    def recover_started_assgined(self, _version, roundStateId, groupId, competitors=["c1","c2","c3"], comments={"c3": None, "c1": None, "c2": None}, ranking={"c3": None, "c1": None, "c2": None}):
        secret_name = os.environ["secretName"]
        region = os.environ["region"]
        a = AppSync_query(secret_name, region)
        a.updateRoundState_started_assigned_query(_version, roundStateId, groupId, competitors, comments, ranking)
        return True
    
    def recover_assgined_queued(self, _version, roundStateId, groupId, competitors=["c1","c2","c3"], comments={"c3": None, "c1": None, "c2": None}, ranking={"c3": None, "c1": None, "c2": None}):
        secret_name = os.environ["secretName"]
        region = os.environ["region"]
        a = AppSync_query(secret_name, region)
        a.updateRoundState_assigned_queued_query(_version, roundStateId, groupId, competitors,comments,ranking)
        return True