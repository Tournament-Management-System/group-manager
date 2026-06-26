import sys
sys.path.append("..")
import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from DAO.tournamentStateDAO import tournamentStateDAO
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db, get_item_db

region = os.environ["region"]
tournamentState_table = os.environ["tournamentState_table"]
group_table = os.environ["group_table"]

class tournamentStateDAOImpl(tournamentStateDAO):
   
    def __init__(self) -> None:
        self.tournamentState_table = boto3.resource("dynamodb", region).Table(tournamentState_table)
        self.groupTable = boto3.resource("dynamodb", region).Table(group_table)        
        self.tournaments = {}
        
    #override
    def getAllTournamentStates(self):
        
        try:
            self.tournaments = scan_items_db(self.tournamentState_table)
        except Exception as err:
            logger.error(
                "Couldn't get all tournaments from table %s. Here's why: %s: %s",
                self.tournamentState_table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.tournaments
    
    #override
    def getTournamentState(self, tournamentStateId):
        
        try:
            tournament = get_item_db(self.tournamentState_table, "tournamentStateId", tournamentStateId)
        except Exception as err:
            logger.error(
                "Couldn't get the tournament from table %s. Here's why: %s: %s",
                self.tournamentState_table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return tournament
    
    #override
    def updateTournamentState(self, tournamentStateId, filed: dict):
        
        try:
            for key in filed:
                update_item_db(self.tournamentState_table, "tournamentStateId", tournamentStateId, key, filed.get(key))
            
        except Exception as err:
            logger.error(
                "Couldn't update the tournament to table %s. Here's why: %s: %s",
                self.tournamentState_table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    
    #override
    def addTournamentState(self, tournamentState):
        
        try:
            put_item_db(self.tournamentState_table, tournamentState)

        except Exception as err:
            logger.error(
                "Couldn't add the tournament to table %s. Here's why: %s: %s",
                self.tournamentState_table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    
    # Override
    def deleteTournamentState(self, tournamentStateId):
        return super().deleteTournament(tournamentStateId)