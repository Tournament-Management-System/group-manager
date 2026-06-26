import sys

sys.path.append("..")
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from aws_helper.DynamoDB import (get_item_db, put_item_db, scan_items_db,
                                 update_item_db)
from DAO.eventStateDAO import eventStateDAO

region = os.environ["region"]
eventState_table = os.environ["eventState_table"]

class eventStateDAOimpl(eventStateDAO):
    def __init__(self) -> None:
        self.eventState_table = boto3.resource("dynamodb", region).Table(eventState_table)
        self.events = []
    
    # Override
    def getAllEventState(self):
        
        try:
            self.events = scan_items_db(self.eventState_table)
        except Exception as err:
            logger.error(
                "Couldn't get all EventSates from table %s. Here's why: %s",
                self.eventState_table,
                str(err))
            raise
        else:
            return self.events
    
    
    # Override
    def getEventState(self, eventSateId):
        
        try:
            event = get_item_db(self.eventState_table, "eventSateId", eventSateId)
        except Exception as err:
            logger.error(
                "Couldn't get the EventSate from table %s. Here's why: %s",
                self.eventState_table,
                str(err))
            raise
        else:
            return event

    # Override
    def updateEventState(self, eventSateId, filed: dict):
        
        try:
            for key in filed:
                update_item_db(self.eventState_table, "eventSateId", eventSateId, key, filed.get(key))
            
        except Exception as err:
            logger.error(
                "Couldn't update the EventSate to table %s. Here's why: %s",
                self.eventState_table,
                str(err))
            raise
        
    # Override
    def deleteEventState(self, eventSateId):
        return super().deleteEvent(eventSateId)
    
    # Override
    def addEventState(self, event):
        
        try:
            put_item_db(self.eventState_table, event)

        except Exception as err:
            logger.error(
                "Couldn't add the EventSate to table %s. Here's why: %s",
                self.eventState_table,
                str(err))
            raise