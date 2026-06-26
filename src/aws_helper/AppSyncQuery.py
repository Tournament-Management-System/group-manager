import json
import os
from boto3 import Session as AWSSession
from dotenv import load_dotenv
from gql import gql
from gql.client import Client
from gql.transport.requests import RequestsHTTPTransport
from requests_aws4auth import AWS4Auth
from aws_helper.secretManager import get_secret
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

load_dotenv()

class AppSync_query():

    def __init__(self, secret_name, region) -> None:
        self.region = region
        self.secret_name = secret_name
        self.client = self.make_client()

    def make_client(self):
        creds = json.loads(get_secret(
            secret_name=self.secret_name, region_name=self.region))
        aws_access_key_id = creds["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = creds["AWS_SECRET_ACCESS_KEY"]
        url = creds["APPSYNC_ENDPOINT"]
        x_api_key = creds["x-api-key"]
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-api-key': x_api_key
        }
        aws = AWSSession(aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name='us-east-1')
        credentials = aws.get_credentials().get_frozen_credentials()

        auth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            aws.region_name,
            'appsync',
            session_token=credentials.token,
        )

        transport = RequestsHTTPTransport(url=url,
                                          headers=headers,
                                          auth=auth)
        client = Client(transport=transport,
                        fetch_schema_from_transport=True)
        return client

    def getRoundState_query(self, inputId):
        myquery = """
        query MyQuery {
            getRoundState(id: "%s") {
                _version
                _lastChangedAt
                _deleted
                assigned
                completed
                createdAt
                eventFormatId
                eventStateId
                id
                queued
                started
                tournamentFormatId
                tournamentStateId
                updatedAt
            }
        }
        """
        try:
            resp = self.client.execute(gql(myquery % inputId))
        except Exception as e:
            logger.debug(str(e))
            raise

        return resp["getRoundState"]

    def getEventFormat_query(self, inputId):
        myquery = """
        query MyQuery {
            getEventFormat(id: "%s") {
                _version
                awards
                createdAt
                id
                _lastChangedAt
                _deleted
                name
                owner
                rounds
                updatedAt
            }
        }    
        """
        try:
            resp = self.client.execute(gql(myquery % inputId))
        except Exception as e:
            logger.debug(str(e))
            raise

        return resp["getEventFormat"]

    def getEventState_query(self, inputId):
        myquery = """
        query MyQuery {
            getEventState(id: "%s") {
                id
                _deleted
                _lastChangedAt
                _version
                awards
                createdAt
                currentRoundIdx
                eventFormatId
                tournamentFormatId
                tournamentStateId
                updatedAt
            }
        }
        """
        try:
            resp = self.client.execute(gql(myquery % inputId))
        except Exception as e:
            logger.debug(str(e))
            raise

        return resp["getEventState"]

    def getVenueId_query(self, inputId):
        myquery = """
        query MyQuery {
            getTournamentFormat(id: "%s") {
                venueId
            }
        }
        """
        try:
            resp = self.client.execute(gql(myquery % inputId))
        except Exception as e:
            logger.debug(str(e))
            raise

        return resp["getTournamentFormat"]["venueId"]

    def updateRoundState_queued_assigned_query(self, variables):
        myquery = """
        mutation updateRoundState($_version : Int, $roundStateId : ID!, $queued : [AWSJSON], $assigned : [AWSJSON]){
            updateRoundState(input: {_version: $_version, id: $roundStateId, queued: $queued, assigned: $assigned}) {
                id
                _deleted
                _lastChangedAt
                _version
                assigned
                completed
                createdAt
                eventFormatId
                eventStateId
                started
                queued
                tournamentFormatId
                tournamentStateId
                updatedAt
            }
        }
        """
        try:
            resp = self.client.execute(
                gql(myquery), variable_values=json.dumps(variables))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp

    def updateRoundState_assigned_started_query(self, variables):
        myquery = """
        mutation updateRoundState($_version : Int, $roundStateId : ID!, $assigned : [AWSJSON], $started : [AWSJSON]){
            updateRoundState(input: {_version: $_version, id: $roundStateId, assigned: $assigned, started: $started}) {
                id
                _deleted
                _lastChangedAt
                _version
                assigned
                completed
                createdAt
                eventFormatId
                eventStateId
                started
                queued
                tournamentFormatId
                tournamentStateId
                updatedAt
            }
        }
        """
        try:
            resp = self.client.execute(
                gql(myquery), variable_values=json.dumps(variables))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp

    def updateRoundState_started_completed_query(self, variables):
        myquery = """
        mutation updateRoundState($_version : Int, $roundStateId : ID!, $started : [AWSJSON], $completed : [AWSJSON] ){
            updateRoundState(input: {_version: $_version, id: $roundStateId, started: $started, completed: $completed}) {
                id
                _deleted
                _lastChangedAt
                _version
                assigned
                completed
                createdAt
                eventFormatId
                eventStateId
                started
                queued
                tournamentFormatId
                tournamentStateId
                updatedAt
            }
        }
        """
        try:
            resp = self.client.execute(
                gql(myquery), variable_values=json.dumps(variables))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp
    def updateRoundState_udpate_all_groups_query(self, variables):
        myquery = """
        mutation updateRoundState($_version : Int, $roundStateId : ID!, $started : [AWSJSON], $completed : [AWSJSON], $assigned : [AWSJSON], $queued : [AWSJSON]){
            updateRoundState(input: {_version: $_version, id: $roundStateId, started: $started, completed: $completed, assigned: $assigned, queued: $queued}) {
                id
                _deleted
                _lastChangedAt
                _version
                assigned
                completed
                createdAt
                eventFormatId
                eventStateId
                started
                queued
                tournamentFormatId
                tournamentStateId
                updatedAt
            }
        }
        """
        try:
            resp = self.client.execute(
                gql(myquery), variable_values=json.dumps(variables))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp
    
    def updateRoundState_started_queued_query(self, _version):

        myquery = """
        mutation updateRoundState($_version : Int, $roundStateId : ID!, $started : [AWSJSON], $queued : [AWSJSON] ){
            updateRoundState(input: {_version: $_version, id: $roundStateId, started: $started, queued: $queued}) {
                assigned
                completed
                createdAt
                eventFormatId
                eventStateId
                id
                tournamentFormatId
                started
                queued
                updatedAt
                tournamentStateId
                _version
            }
        }
        """
        variables = {
            'roundStateId': "assigntostartid",
            'queued': [json.dumps({"competitors": ["c1", "c2", "c3"], "comments":{"c3": None, "c1": None, "c2": None}, "groupId": 0, "ranking": {"c3": None, "c1": None, "c2": None}, "judges": [], "roomId":None})],
            'started': [],
            '_version': _version,
        }
        try:
            resp = self.client.execute(
                gql(myquery), variable_values=json.dumps(variables))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp

    def updateRoundState_started_assigned_query(self, _version, roundStateId, groupId, competitors, comments, ranking):
        myquery = """
        mutation updateRoundState($_version : Int, $roundStateId : ID!, $started : [AWSJSON], $assigned : [AWSJSON], $queued: [AWSJSON] ){
            updateRoundState(input: {_version: $_version, id: $roundStateId, started: $started, assigned: $assigned, queued: $queued}) {
                assigned
                completed
                createdAt
                eventFormatId
                eventStateId
                id
                tournamentFormatId
                started
                queued
                updatedAt
                tournamentStateId
                _version
            }
        }
        """
        variables = {
            'roundStateId': roundStateId,
            'assigned': [json.dumps({"competitors": competitors, "comments":comments, "groupId": groupId, "ranking": ranking, "judges": [], "roomId":None})],
            'started': [],
            'queued': [],
            'completed': [],
            '_version': _version,
        }
        try:
            resp = self.client.execute(
                gql(myquery), variable_values=json.dumps(variables))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp
    def updateRoundState_assigned_queued_query(self, _version, roundStateId, groupId, competitors, comments, ranking):
        myquery = """
        mutation updateRoundState($_version : Int, $roundStateId : ID!, $started : [AWSJSON], $assigned : [AWSJSON], $queued: [AWSJSON] ){
            updateRoundState(input: {_version: $_version, id: $roundStateId, started: $started, assigned: $assigned, queued: $queued}) {
                assigned
                completed
                createdAt
                eventFormatId
                eventStateId
                id
                tournamentFormatId
                started
                queued
                updatedAt
                tournamentStateId
                _version
            }
        }
        """
        variables = {
            'roundStateId': roundStateId,
            'queued': [json.dumps({"competitors": competitors, "comments":comments, "groupId": groupId, "ranking": ranking, "judges": [], "roomId":None})],
            'started': [],
            'assigned': [],
            'completed': [],
            '_version': _version,
        }
        try:
            resp = self.client.execute(
                gql(myquery), variable_values=json.dumps(variables))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp
    
    def getTournamentState_query(self, tournamentStateId):
        myquery = """
        query MyQuery {
            getTournamentState(id: "%s") {
                _deleted
                _lastChangedAt
                _version
                competitors
                createdAt
                eventFormatIds
                id
                rooms
                judges
                tournamentFormatId
                updatedAt
            }
        }
        """    
        try:
            resp = self.client.execute(gql(myquery % tournamentStateId))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp
    
    def update_judges_rooms_TournamentState_query(self, tournamentStateId, _version, judges, rooms):
        myquery="""
        mutation updateTournamentState($_version: Int, $tournamentStateId: ID!, $judges: AWSJSON, $rooms: AWSJSON){
            updateTournamentState(input: {id: $tournamentStateId, _version: $_version, judges: $judges, rooms: $rooms}) {
                _version
                id
                rooms
                judges
            }
        }
        """
        variables = {
            'tournamentStateId': tournamentStateId,
            '_version': _version,
            'judges': judges,
            'rooms': rooms
        }
        try:
            resp = self.client.execute(
                gql(myquery), variable_values=json.dumps(variables))
        except Exception as e:
            logger.debug(str(e))
            raise
        return resp
    
    
    # Need to json dump the inner dict, below is an example
"""
variables = {'roundStateId' : "300ccfcd-433d-4616-8f9b-45062de419eb", 
        '_version': 12,
        'queued' : [json.dumps({"competitors":["c1","c2","c3"],"comments":{"c3":None,"c1":None,"c2":None},"groupId":0,"ranking":{"c3":None,"c1":None,"c2":None},"judges":[],"roomId":None}),
                    json.dumps({"competitors":["c4","c5","c6"],"comments":{"c4":None,"c5":None,"c6":None},"groupId":1,"ranking":{"c4":None,"c5":None,"c6":None},"judges":[],"roomId":None}), 
                    json.dumps({"competitors":["c7","c8","c9"],"comments":{"c7":None,"c8":None,"c9":None},"groupId":2,"ranking":{"c7":None,"c8":None,"c9":None},"judges":[],"roomId":None}), 
                    json.dumps({"competitors":["ca","cb","cc"],"comments":{"cc":None,"ca":None,"cb":None},"groupId":3,"ranking":{"cc":None,"ca":None,"cb":None},"judges":[],"roomId":None}),
                    json.dumps({"competitors":["cd","ce","cf"],"comments":{"cd":None,"ce":None,"cf":None},"groupId":4,"ranking":{"cd":None,"ce":None,"cf":None},"judges":[],"roomId":None}),
                    json.dumps({"competitors":["cg","c0","ch"],"comments":{"cg":None,"ch":None,"c0":None},"groupId":5,"ranking":{"cg":None,"ch":None,"c0":None},"judges":[],"roomId":None})],
        'started': []
        }
"""
"""
variables = {'_version': 1, '_lastChangedAt': 1668476554596, '_deleted': None,
             'assigned': [{"competitors": ["c1", "c2", "c3"], "comments":{"c3": None, "c1": None, "c2": None}, "groupId": 0, "ranking": {"c3": None, "c1": None, "c2": None}, "judges": [], "roomId":None}],
             'completed': [],
             'createdAt': '2022-11-15T01:42:34.570Z',
             'eventFormatId': 'simpleeventformatid',
             'eventStateId': 'simpleeventstateid',
             'id': 'simpleroundstateid',
             'queued': [],
             'started': None,
             'tournamentFormatId': 'simpletournameformatid',
             'tournamentStateId': 'simpletournamentstateid',
             'updatedAt': '2022-11-15T01:42:34.570Z'}
"""
