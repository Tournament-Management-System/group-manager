import sys 
sys.path.append("..")
import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from DAO.GroupDAO import GroupDAO
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db, get_item_db

region = os.environ["region"]
group_table = os.environ["group_table"]

class GroupDAOimpl(GroupDAO):
   
    def __init__(self) -> None:
        self.groupTable = boto3.resource("dynamodb", region).Table(group_table)
        self.groups = {}
        
    # Override
    def getAllGroups(self):
        
        try:
            self.groups = scan_items_db(self.groupTable)
        except Exception as err:
            logger.error(
                "Couldn't get all groups from table %s. Here's why: %s: %s",
                self.groupTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.groups
        
    # Override
    def getGroup(self, groupId):
        
        try:
            group = get_item_db(self.groupTable, "groupId", groupId)
        except Exception as err:
            logger.error(
                "Couldn't get the group from table %s. Here's why: %s: %s",
                self.groupTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return group
    
    # Override
    def updateGroup(self, groupId, filed: dict):
        try:
            for key in filed:
                update_item_db(self.groupTable, "groupId", groupId, key, filed.get(key))
            
        except Exception as err:
            logger.error(
                "Couldn't update the group to table %s. Here's why: %s: %s",
                self.groupTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        

    # Override
    def deleteGroup(self, groupId):
        pass
    
    # Override
    def addGroup(self, group):
        
        try:
            put_item_db(self.groupTable, group)

        except Exception as err:
            logger.error(
                "Couldn't add the group to table %s. Here's why: %s",
                self.groupTable,
                str(err))
            raise
        
    # Override
    def getGroupsbyRoundId(self, roundId):
        
        try:
            self.groups = scan_items_db(self.groupTable)
            list = []
            for groups in self.groups:
                if groups.get("roundId") == roundId:
                    list.append(groups)
            if list:
                return list
            
        except Exception as err:
            logger.error(
                "Couldn't get the group from table %s. Here's why: %s: %s",
                self.groupTable,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        
        else:
            return None
        
