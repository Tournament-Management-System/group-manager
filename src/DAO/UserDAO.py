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

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

class UserDAO():
    def __init__(self):
        self.eventTable = boto3.resource('dynamodb', region).Table(eventTable)
        self.userTable = boto3.resource('dynamodb', region).Table(userTable)
        self.tournamentTable = boto3.resource('dynamodb', region).Table(tournamentTable)

    def getUser(self, userId: str):
        try:
            user = get_item_db(self.userTable, "userId", userId)
        except Exception as e:
            logger.error("[userDAO] Error getting user: userId %s, message %s", userId, e['Error']['Message'])
            raise
        else:
            return user
    
    def updateUser(self, userId, fields: dict):
        try:
            for key in fields:
                update_item_db(self.userTable, 'userId', userId, key, fields.get(key))
        except Exception as e:
            logger.error('[userDAO] Error updating user %s in table %s: %s',
            userId, self.userTable, e['Error']['Message'])
            raise