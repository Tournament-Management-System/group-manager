import sys
sys.path.append("..")
import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from DAO.roundStateDAO import roundStateDAO
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db, get_item_db

region = os.environ["region"]
roundState_table = os.environ["roundState_table"]
group_table = os.environ["group_table"]

class roundStateImpl(roundStateDAO):
   
    def __init__(self) -> None:
        self.roundState_table = boto3.resource("dynamodb", region).Table(roundState_table)
        self.groupTable = boto3.resource("dynamodb", region).Table(group_table)        
        self.rounds = {}
        
    #override
    def getAllRoundStates(self):
        
        try:
            self.rounds = scan_items_db(self.roundState_table)
        except Exception as err:
            logger.error(
                "Couldn't get all rounds from table %s. Here's why: %s: %s",
                self.roundState_table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.rounds
    
    #override
    def getRoundState(self, roundStateId):
        
        try:
            round = get_item_db(self.roundState_table, "roundStateId", roundStateId)
        except Exception as err:
            logger.error(
                "Couldn't get the round from table %s. Here's why: %s: %s",
                self.roundState_table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return round
    
    #override
    def updateRoundState(self, roundStateId, filed: dict):
        
        try:
            for key in filed:
                update_item_db(self.roundState_table, "roundStateId", roundStateId, key, filed.get(key))
            
        except Exception as err:
            logger.error(
                "Couldn't update the round to table %s. Here's why: %s: %s",
                self.roundState_table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    
    #override
    def addRoundState(self, roundState):
        
        try:
            put_item_db(self.roundState_table, roundState)

        except Exception as err:
            logger.error(
                "Couldn't add the round to table %s. Here's why: %s: %s",
                self.roundState_table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    