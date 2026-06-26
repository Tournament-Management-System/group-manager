import sys 
sys.path.append("..")
import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from DAO.tournamentFormatDAO import tournamentFormatDAO
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db, get_item_db

region = os.environ["region"]
tournamentFormat_table = os.environ["tournamentFormat_table"]

class tournamentFormatDAOimpl(tournamentFormatDAO):
    def __init__(self) -> None:
        self.tournamentFormat_table = boto3.resource("dynamodb", region).Table(tournamentFormat_table)
        self.tournaments = []
    
    # Override
    def getAllTournamentFormat(self):
        
        try:
            self.tournaments = scan_items_db(self.tournamentFormat_table)
        except Exception as err:
            logger.error(
                "Couldn't get all tournamentFormats from table %s. Here's why: %s",
                self.tournamentFormat_table,
                str(err))
            raise
        else:
            return self.tournaments
    
    
    # Override
    def getTournamentFormat(self, tournamentFormatId):
        
        try:
            tournament = get_item_db(self.tournamentFormat_table, "tournamentFormatId", tournamentFormatId)
        except Exception as err:
            logger.error(
                "Couldn't get the tournamentFormat from table %s. Here's why: %s",
                self.tournamentFormat_table,
                str(err))
            raise
        else:
            return tournament

    # Override
    def updateTournamentFormat(self, tournamentFormatId, filed: dict):
        
        try:
            for key in filed:
                update_item_db(self.tournamentFormat_table, "tournamentFormatId", tournamentFormatId, key, filed.get(key))
            
        except Exception as err:
            logger.error(
                "Couldn't update the tournamentFormat to table %s. Here's why: %s",
                self.tournamentFormat_table,
                str(err))
            raise
        
    # Override
    def deleteTournamentFormat(self, tournamentFormatId):
        return super().deleteTournament(tournamentFormatId)
    
    # Override
    def addTournamentFormat(self, tournament):
        
        try:
            put_item_db(self.tournamentFormat_table, tournament)

        except Exception as err:
            logger.error(
                "Couldn't add the tournamentFormat to table %s. Here's why: %s",
                self.tournamentFormat_table,
                str(err))
            raise