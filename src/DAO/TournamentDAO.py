import sys
import os
import boto3
import logging
sys.path.append('..')
from aws_helper.DynamoDB import update_item_db, scan_items_db, get_item_db, put_item_db

region = os.environ['region']
tournamentTable = os.environ['tournament_table']
eventTable = os.environ['event_table']
userTable = os.environ['user_table']
roomTable = os.environ['room_table']

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

class TournamentDAO():
    def __init__(self):
        self.eventTable = boto3.resource('dynamodb', region).Table(eventTable)
        self.roomTable = boto3.resource('dynamodb', region).Table(roomTable)
        self.userTable = boto3.resource('dynamodb', region).Table(userTable)
        self.tournamentTable = boto3.resource('dynamodb', region).Table(tournamentTable)

    def getTournament(self, tournamentId: str):
        try:
            tournament = get_item_db(self.tournamentTable, "tournamentId", tournamentId)
        except Exception as e:
            logger.error("[tournamentDAO] Error getting tournament: tournamentId %s, message %s", tournamentId, e['Error']['Message'])
            raise
        else:
            return tournament

    def getEvent(self, tournamentId: str, eventId: str):
        try:
            tournament = get_item_db(self.tournamentTable, "tournamentId", tournamentId)
            for event in tournament.get('eventsIds'):
                if event == eventId:
                    event_ = get_item_db(self.eventTable, "eventId", eventId)
                    return event_
        except Exception as e:
            logger.error("[tournamentDAO] Error getting event: tournamentId %s, eventId %d, message %s", tournamentId, eventId, e['Error']['Message'])
            raise
        else:
            return event
    
    def getJudges(self, tournamentId: str):
        try:
            tournament = get_item_db(self.tournamentTable, "tournamentId", tournamentId)
            judges = []
            for judge in tournament.get('judges'):
                judges.append(judge)
        except Exception as e:
            logger.error("[tournamentDAO] Error getting judges: tournamentId %s, message %s", tournamentId, e['Error']['Message'])
            raise
        else:
            return judges

    def updateTournament(self, tournamentId, fields: dict):
        try:
            for key in fields:
                update_item_db(self.roomTable, 'tournamentId', tournamentId, key, fields.get(key))
        except Exception as e:
            logger.error('[tournamentDAO] Error updating tournament %s in table %s: %s',
            tournamentId, self.roomTable, e['Error']['Message'])
            raise
    
    def createTournament(self, tournament):
        try:
            put_item_db(self.tournamentTable, tournament)
        except Exception as e:
            logger.error('[tournamentDAO] Error creating tournament in table %s: %s', self.roomTable, e['Error']['Message'])