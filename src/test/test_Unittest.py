from moto import mock_dynamodb, mock_lambda
import unittest
from unittest import mock
import json
import boto3
from decimal import Decimal
from aws_helper.AppSyncQuery import AppSync_query
from aws_helper.DynamoDB import get_item_db, put_item_db, get_items_db, update_item_db
from test.mock_lambda import mock_some_lambda, lambda_getAvailableRooms

_version = 1
class test_Unittest(unittest.TestCase):

    def test_getRoundState_query(self):
        a = AppSync_query()
        response = a.getRoundState_query("simpleroundstateid")
        assert response == {'_version': _version, '_lastChangedAt': 1668476554596, '_deleted': None, 'assigned': [], 'completed': [], 'createdAt': '2022-11-15T01:42:34.570Z', 'eventFormatId': 'simpleeventformatid', 'eventStateId': 'simpleeventstateid', 'id': 'simpleroundstateid', 'queued': ['{"competitors":["c1","c2","c3"],"comments":{"c3":null,"c1":null,"c2":null},"groupId":0,"ranking":{"c3":null,"c1":null,"c2":null},"judges":[],"roomId":null}'], 'started': None, 'tournamentFormatId': 'simpletournameformatid', 'tournamentStateId': 'simpletournamentstateid', 'updatedAt': '2022-11-15T01:42:34.570Z'}
    
    def test_getEventFormat_query(self):
        a = AppSync_query()
        response = a.getEventFormat_query("simpleeventformatid")
        assert response == {'id': 'simpleeventformatid', 'awards': [], 'name': 'testeventformat', 'owner': None, 'rounds': ['{"roundIndex":0,"competitorLimit":null,"judgesPerRound":1,"judgingCriteria":null,"groupLimit":6}'], '_deleted': None, '_lastChangedAt': 1668477111722, '_version': _version}
    
    def test_getEventState_query(self):
        a = AppSync_query()
        response = a.getEventState_query("simpleeventstateid")
        assert response == {'id': 'simpleeventstateid', '_deleted': None, '_lastChangedAt': 1668476717569, '_version': _version, 'awards': [], 'createdAt': '2022-11-15T01:45:17.544Z', 'currentRoundIdx': 0, 'eventFormatId': 'simpleeventformatid', 'tournamentFormatId': 'simpletournameformatid', 'tournamentStateId': 'simpletournamentstateid', 'updatedAt': '2022-11-15T01:45:17.544Z'}
    
    """
    def test_put_get_item_happy(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table_name = 'test_event_table'
        event_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'eventId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'eventId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        event_meta_data_file_name = '.test.eventMetaData.json'
        with open(event_meta_data_file_name) as data:
            event_meta_data = json.load(data, parse_float=Decimal)
        #event_data = eventMetaData()
        put_item_db(event_table, event_meta_data)
        response =  get_item_db(event_table, "eventId", event_meta_data["eventId"])
        assert event_meta_data == response

    def test_update_item_happy(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table_name = 'test_event_table'
        event_table = dynamodb.create_table(TableName=table_name,
                KeySchema=[{'AttributeName': 'eventId','KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'eventId','AttributeType': 'S'}],
                ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5  
        })
        event_meta_data_file_name = '.test.eventMetaData.json'
        with open(event_meta_data_file_name) as data:
            event_meta_data = json.load(data, parse_float=Decimal)
        #event_data = eventMetaData()
        put_item_db(event_table, event_meta_data)
        update_item_db(event_table, "eventId", event_meta_data["eventId"], "currentRoundIdx", 3)
        response =  get_item_db(event_table, "eventId", event_meta_data["eventId"])
        assert response["currentRoundIdx"] == 3
    
    def test_lambda_happy(self):
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        mock_some_lambda(lambda_client,"getAvailableRooms", lambda_getAvailableRooms())
        
        available_room_event = {
        "body": {
            "tournamentId" : "test111"
            }
        }#dict
        available_room_response = lambda_client.invoke(
            FunctionName='getAvailableRooms',
            InvocationType='Event',
            Payload=json.dumps(available_room_event),
        )
        room_payload = json.loads(available_room_response["Payload"].read())
        assert room_payload["body"]["totalRoom"] == 3
        assert room_payload["body"]["rooms"] == ["r1", "r2", "r3"]
    """