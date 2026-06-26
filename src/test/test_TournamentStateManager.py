from aws_helper.graphQLCommon import *
from src.Lambda.TournamentStateManager import *
import logging
from decimal import Decimal
import pytest
import boto3
import unittest
import json
import sys
import os
sys.path.append("../..")
# @mock_lambda_tournament

tournamentForamtId = ""
tournamentStateId = ""
eventFormatId = ""
judgeId = ""
venueId = ""
roomId = ""

"""
class test_TournamentStateManager(unittest.TestCase):

    def test_startTournamentHandler_happy(self):
        event = {
            "body": {
                "tournamentFormatId": tournamentForamtId,
            }
        }
        response = startTournamentHandler(event, "")
        logging.info(response)
        assert response["statusCode"] == 200

    def test_completeTournamentHandler_happy(self):
        event = {
            "body": {
                "tournamentFormatId": tournamentForamtId,
            }
        }
        response = completeTournamentHandler(event, "")
        assert response["statusCode"] == 200

    def test_startEventHandler_happy(self):
        event = {
            "body": {
                "tournamentStateId": tournamentStateId,
                "eventFormatId": eventFormatId,
            }
        }
        response = startEventHandler(event, "")
        assert response["statusCode"] == 200

    def test_completeEventHandler_happy(self):
        event = {
            "body": {
                "tournamentStateId": tournamentStateId,
                "eventFormatId": eventFormatId,
            }
        }
        response = completeEventHandler(event, "")
        assert response["statusCode"] == 200

    def test_startRoomHandler_happy(self):
        event = {
            "body": {
                "roomId": roomId,
            }
        }
        response = startRoomHandler(event, "")
        assert response["statusCode"] == 200

    def test_completeRoomHandler_happy(self):
        event = {
            "body": {
                "roomId": roomId,
            }
        }
        response = completeRoomHandler(event, "")
        assert response["statusCode"] == 200

    def test_freeJudgeHandler_happy(self):
        event = {
            "body": {
                "judgeId": judgeId,
                "tournamentFormatId": tournamentForamtId,
            }
        }
        response = freeJudgeHandler(event, "")
        assert response["statusCode"] == 200

    def test_useJudgeHandler_happy(self):
        event = {
            "body": {
                "judgeId": judgeId,
                "tournamentFormatId": tournamentForamtId,
            }
        }
        response = useJudgeHandler(event, "")
        assert response["statusCode"] == 200

    def test_getAvailableJudgesHandler_happy(self):
        event = {
            "body": {
                "tournamentStateId": tournamentStateId,
            }
        }
        response = getAvailableJudgesHandler(event, "")
        assert response["statusCode"] == 200

    def test_getAvailableRoomsHandler_happy(self):
        event = {
            "body": {
                "tournamentFormatId": tournamentForamtId,
            }
        }
        response = getAvailableRoomsHandler(event, "")
        assert response["statusCode"] == 200

    def test_getEventCompetitorsHandler_happy(self):
        event = {
            "body": {
                "tournamentFormatId": tournamentForamtId,
                "tournamentStateId": tournamentStateId,
            }
        }
        response = getAvailableRoomsHandler(event, "")
        assert response["statusCode"] == 200
"""
