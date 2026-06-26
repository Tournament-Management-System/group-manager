import sys 
sys.path.append("..")
import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from DAO.eventFormatDAO import eventFormatDAO
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db, get_item_db

region = os.environ["region"]
eventFormat_table = os.environ["eventFormat_table"]

class eventFormatDAOimpl(eventFormatDAO):
    def __init__(self) -> None:
        self.eventFormat_table = boto3.resource("dynamodb", region).Table(eventFormat_table)
        self.events = []
    
    # Override
    def getAllEventFormat(self):
        
        try:
            self.events = scan_items_db(self.eventFormat_table)
        except Exception as err:
            logger.error(
                "Couldn't get all eventFormats from table %s. Here's why: %s",
                self.eventFormat_table,
                str(err))
            raise
        else:
            return self.events
    
    
    # Override
    def getEventFormat(self, eventFormatId):
        
        try:
            event = get_item_db(self.eventFormat_table, "eventFormatId", eventFormatId)
        except Exception as err:
            logger.error(
                "Couldn't get the eventFormat from table %s. Here's why: %s",
                self.eventFormat_table,
                str(err))
            raise
        else:
            return event

    # Override
    def updateEventFormat(self, eventFormatId, filed: dict):
        
        try:
            for key in filed:
                update_item_db(self.eventFormat_table, "eventFormatId", eventFormatId, key, filed.get(key))
            
        except Exception as err:
            logger.error(
                "Couldn't update the eventFormat to table %s. Here's why: %s",
                self.eventFormat_table,
                str(err))
            raise
        
    # Override
    def deleteEventFormat(self, eventFormatId):
        return super().deleteEvent(eventFormatId)
    
    # Override
    def addEventFormat(self, event):
        
        try:
            put_item_db(self.eventFormat_table, event)

        except Exception as err:
            logger.error(
                "Couldn't add the eventFormat to table %s. Here's why: %s",
                self.eventFormat_table,
                str(err))
            raise