from src.test.mock_lambda import mock_some_lambda, lambda_getAvailableRooms, lambda_getAvailableJudges, lambda_normal
from src.test.TestData import roundData_startCompetition, roundData_startGroups, roundData_collectResult, eventMetaData, groupData
from aws_helper.DynamoDB import get_item_db, put_item_db, get_items_db
from src.Lambda.GroupManager import startGroups_handler, startCompetition_handler, collectResult_handler
from src.Lambda.groupUtils import groupUtils
from aws_helper.AppSyncQuery import AppSync_query
from moto import mock_dynamodb, mock_lambda
import logging
from decimal import Decimal
import pytest
import boto3
from unittest import mock
import unittest
import json
import sys
import os
sys.path.append("../..")
# @mock_lambda

roundStateId = "4d79308c-aa65-43b6-9683-c91ec42a3ff9"
groupId = 1
ranking =  {"cd":48, "ce":55,"cf":56}
_version = 24
class test_GroupManager(unittest.TestCase):
    
    def test_startGroups_handler_happy(self):
        event = {
            "body": {
                "roundStateId": roundStateId,

            }
        }
        response = startGroups_handler(event, "")
        logging.info(response)
        assert response["statusCode"] == 200
    
    """
    def test_startCompetition_handler_happy(self):
        event = {
            "body": {
                "roundStateId": roundStateId,
                "groupId": groupId
            }
        }
        secret_name = os.environ["secretName"]
        region = os.environ["region"]
        response = startCompetition_handler(event, "")
        assert response["statusCode"] == 200

        _version = int(response["body"]) + 1
        print(_version)
        #a = AppSync_query(secret_name, region)
        #a.updateRoundState_started_assigned_query(_version)
    """
    """
    def test_collectResult_handler(self):
        event = {
            "body":{
                "roundStateId": roundStateId,
                "groupId": groupId,
                "ranking": ranking

            }
        }
        response = collectResult_handler(event, "")
        assert response["statusCode"] == 400
    """
    """
    def test_recover_started_assgined(self):
        GROUPUtils = groupUtils()
        response = GROUPUtils.recover_started_assgined(_version, roundStateId, groupId)
        assert response
    """
    """
    def test_recover_assgined_queued(self):
        GROUPUtils = groupUtils()
        response = GROUPUtils.recover_assgined_queued(_version, roundStateId, groupId, ["ca","cb","cc"], {"ca":None, "cb":None, "cc":None}, {"ca":None, "cb":None, "cc":None})
        assert response
    """
            