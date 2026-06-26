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

class RoomDAO():
    def __init__(self):
        self.eventTable = boto3.resource('dynamodb', region).Table(eventTable)
        self.roomTable = boto3.resource('dynamodb', region).Table(roomTable)
        self.userTable = boto3.resource('dynamodb', region).Table(userTable)

    def getCompetitors(self, roomId: str):
        try:
            room = get_item_db(self.roomTable, "roomId", roomId)
        except Exception as e:
            logger.error("[roomDAO] Error getting competitors: roomId %s, message %s", roomId, e['Error']['Message'])
            raise
        else:
            return room.get('competitors')
    
    def getRoom(self, roomId: str):
        try:
            room = get_item_db(self.roomTable, "roomId", roomId)
        except Exception as e:
            logger.error("[roomDAO] Error getting room: roomId %s, message %s", roomId, e['Error']['Message'])
            raise
        else:
            return room

    def getJudges(self, roomId):
        try:
            room = get_item_db(self.roomTable, "roomId", roomId)
        except Exception as e:
            logger.error("[roomDAO] Error getting judges: roomId %s, message %s", roomId, e['Error']['Message'])
            raise
        else:
            return room.get('judges')

    def updateRoom(self, roomId, fields: dict):
        try:
            for key in fields:
                update_item_db(self.roomTable, 'roomId', roomId, key, fields.get(key))
        except Exception as e:
            logger.error('[roomDAO] Error updating room %s in table %s: %s',
            roomId, self.roomTable, e['Error']['Message'])
            raise
    
    def createRoom(self, room):
        try:
            put_item_db(self.roomTable, room)
        except Exception as e:
            logger.error('[roomDAO] Error creating room in table %s: %s', self.roomTable, e['Error']['Message'])