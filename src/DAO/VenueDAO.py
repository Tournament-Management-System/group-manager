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
venueTable = os.environ['venue_table']

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

class VenueDAO():
    def __init__(self):
        self.eventTable = boto3.resource('dynamodb', region).Table(eventTable)
        self.roomTable = boto3.resource('dynamodb', region).Table(roomTable)
        self.userTable = boto3.resource('dynamodb', region).Table(userTable)
        self.venueTable = boto3.resource('dynamodb', region).Table(venueTable)
    
    def getVenue(self, venueId: str):
        try:
            venue = get_item_db(self.venueTable, "venueId", venueId)
        except Exception as e:
            logger.error("[VenueDAO] Error getting venue: venueId %s, message %s", venueId, e['Error']['Message'])
            raise
        else:
            return venue

    def getAllVenues(self):
        try:
            venues = scan_items_db(self.venueTable)
        except Exception as e:
            logger.error("[VenueDAO] Error getting all venues: message %s" e['Error']['Message'])
            raise
        else:
            return venues

    def updateVenue(self, venueId, fields: dict):
        try:
            for key in fields:
                update_item_db(self.venueTable, 'venueId', venueId, key, fields.get(key))
        except Exception as e:
            logger.error('[VenueDAO] Error updating venue %s in table %s: %s',
            venueId, self.venueTable, e['Error']['Message'])
            raise
    
    def createVenue(self, venue):
        try:
            put_item_db(self.venueTable, venue)
        except Exception as e:
            logger.error('[VenueDAO] Error creating room in table %s: %s', self.venueTable, e['Error']['Message'])