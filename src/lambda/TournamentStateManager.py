import logging
import boto3
import json
import os
import random
from constants.Response import returnResponse
from constants.CommonPrints import printContext, printEvent
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db
from aws_helper.appsync import query
from aws_helper.graphQLCommon import *
from gql import gql
from dotenv import load_dotenv


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

lambda_client = boto3.client('lambda', region_name='us-east-1')

# start a tournament
# create a tournament state and event states for each event format


def startTournamentHandler(event, context):
    printEvent(event, 'startTournamentHandler')
    printContext(event, 'startTournamentHandler')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    if body.get('tournamentFormatId') == None:
        return returnResponse(400, {'message': 'query is invalid. Requires tournamentFormatId'})

    tournamentFormatId = body['tournamentFormatId']
    tournamentFormat = getTournamentFormat(tournamentFormatId)

    if tournamentFormat == None:
        return returnResponse(400, {'message': 'query is wrong', 'tournamentFormatId': tournamentFormatId})

    logger.debug('[startTournamentHandler] tournamentFormat: {}'.format(
        json.dumps(tournamentFormat)))

    # create tournament state
    competitorEntries = []
    for competitor in tournamentFormat['competitionEntries']['items']:
        c = getCompetitorEntry(competitor['id'])
        if c['_deleted'] != True:
            competitorEntries.append(
                {'competitorEntryId': competitor['id'], 'active': True})
    print()
    print(competitorEntries)

    judges = []
    for judge in tournamentFormat['judges']['items']:
        judges.append({'judgeId': judge['id'], 'assigned': False})
    print()
    print(judges)
    print()

    rooms = []
    venue = getVenue(tournamentFormat['venueId'])
    logger.debug('[startTournamentHandler] venue {}: {}'.format(
        tournamentFormat['venueId'], json.dumps(venue)))
    for room in venue['rooms']:
        rooms.append({'roomId': room, 'available': True})
    logger.debug('[startTournamentHandler] rooms {}: {}'.format(
        tournamentFormat['venueId'], json.dumps(rooms)))

    print(tournamentFormat)

    myQuery = """
mutation MyMutation($eventFormatIds: [ID], $competitors: AWSJSON, $judges: AWSJSON , $tournamentFormatId: ID!, $_version: Int, $rooms: AWSJSON) {
createTournamentState(input: {_version: $_version, competitors: $competitors, eventFormatIds: $eventFormatIds, judges: $judges, tournamentFormatId: $tournamentFormatId, rooms: $rooms}) {
id 
updatedAt 
tournamentFormatId 
judges 
rooms 
eventFormatIds 
createdAt 
competitors 
_version 
_lastChangedAt 
_deleted 
eventState { 
items { 
id 
}
}
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    variables = {
        '_version': str(10),
        'competitors': json.dumps(competitorEntries),
        'eventFormatIds': json.dumps(tournamentFormat['eventFormatIds']),
        'judges': json.dumps(judges),
        'tournamentFormatId': tournamentFormat['id'],
        'rooms': json.dumps(rooms),
    }
    tournamentState = query(myQuery, variables)
    tournamentState = tournamentState['createTournamentState']
    print(tournamentState)
    logger.debug('[startTournamentHandler] tournamentState {}: {}'.format(
        tournamentState['id'], json.dumps(tournamentState)))

    tournamentFormat['tournamentFormatTournamentStateId'] = tournamentState['id']

    print()
    print(tournamentFormat)
    updateTournamentFormat(tournamentFormat, tournamentFormat['_version'])

    # Call startrounds to create the eventStates
    for eventFormatId in tournamentFormat['eventFormatIds']:
        eventFormat = getEventFormat(eventFormatId)
        if eventFormat == None:
            logger.error('tournamentFormat %s has invalid eventFormatId %s',
                         tournamentFormat['id'], eventFormatId)
            return returnResponse(500, {'message': 'invalid eventFormatId', 'tournamentFormatId': tournamentFormat['id'], 'eventFormatId': eventFormatId})

        startEventEvent = {
            "body": {
                'eventFormatId': eventFormatId,
                'tournamentStateId': tournamentState['id'],
                'tournamentFormatId': tournamentFormatId,
            },
        }
        startEventResponse = lambda_client.invoke(FunctionName='TournamentManagementStack-startEventHandlerBEE0E31-QJfGjz4U0Hxh',
                                                  InvocationType='RequestResponse',
                                                  Payload=json.dumps(startEventEvent),)
        logger.debug('[startTournamentHandler] startEventResponse: {}'.format(
            startEventResponse))
        startEventPayload = startEventResponse['Payload']
        startEventPayload = json.loads(startEventPayload.read())
        logger.debug(
            '[startTournamentHandler] payload: {}'.format(startEventPayload))
        if (startEventPayload['statusCode'] >= 300 or startEventPayload['statusCode'] < 200):
            logger.error('[startTournamentHandler] Unable to start event: {}'.format(
                startEventResponse))
            return returnResponse(startEventPayload['statusCode'], {'message': startEventPayload, 'eventFormatId': event})

    # get venue
    # venue = getVenue(tournamentFormat['venueId'])
    # if venue == None:
    #     logger.error('tournamentFormat %s has invalid venueId %s', tournamentFormat['id'], tournamentFormat['venueId'])
    #     return returnResponse(500, {'message': 'invalid venueId', 'tournamentFormatId': tournamentFormat['id'], 'venueId': tournamentFormat['venueId']})

    # logger.debug('[startTournamentHandler] venue: {}'.format(json.dumps(venue)))

    # rooms = venue['rooms']
    # if (len(rooms) == 0):
    #     logger.error('[startTournamentHandler] invalid venue rooms: %s', venue.get('id'))
    #     return returnResponse(500, {'message': 'Venue[rooms] is NULL'})
    # # set room statuses to inactive until event starts
    # i = 0
    # for room in rooms:
    #     judges = []
    #     competitors = []
    #     room_ = getRoom(room)
    #     updateRoom(room, 'INACTIVE', room_['_version'], judges, competitors)
    #     logger.debug('[startTournamentHandler] roomUpdated: {}'.format(i))
    #     i+=1

    return returnResponse(200, {'message': 'tournament started', 'tournamentFormatId': tournamentFormat['id'], 'tournamentStateId': tournamentFormat['tournamentFormatTournamentStateId'], 'competitors': competitorEntries})

# complete a tournament
# mark all rooms, all judges, and all competitors as inactive


def completeTournamentHandler(event, context):
    printEvent(event, 'completeTournamentHandler')
    printContext(event, 'completeTournamentHandler')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    if body.get('tournamentFormatId') == None:
        return returnResponse(400, {'message': 'query is invalid. Requires tournamentFormatId'})

    tournamentFormatId = body['tournamentFormatId']
    tournamentFormat = getTournamentFormat(tournamentFormatId)
    if tournamentFormat == None:
        return returnResponse(400, {'message': 'query is wrong', 'tournamentFormatId': tournamentFormatId})

    logger.debug('[completeTournamentHandler] tournamentFormatId: {}'.format(
        tournamentFormatId))

    tournamentState = getTournamentState(
        tournamentFormat['tournamentFormatTournamentStateId'])
    if tournamentState == None:
        return returnResponse(400, {'message': 'tournamentState does not exist', 'tournamentStateId': tournamentFormat['tournamentFormatTournamentStateId']})

    judges = json.loads(tournamentState['judges'])
    while (type(judges) == str):
        judges = json.loads(judges)

    logger.debug('[completeTournamentHandler] tournamentState: {}'.format(
        json.dumps(tournamentState)))

    # set judges as inactive
    for judge in judges:
        judge['assigned'] = False

    tournamentState['judges'] = json.dumps(judges)

    # set competitors as inactive
    competitorEntries = json.loads(tournamentState['competitors'])
    while (type(competitorEntries) == str):
        competitorEntries = json.loads(competitorEntries)

    print(competitorEntries)
    for competitorEntry in competitorEntries:
        competitorEntry['active'] = False

    tournamentState['competitors'] = json.dumps(competitorEntries)
    print()
    print('tournamentSTate')
    print(tournamentState)
    if (updateTournamentState(tournamentState, tournamentState['_version']) == False):
        return returnResponse(500, {'message': 'failed to update tournamentState', 'tournamentStateId': tournamentState['id'], 'tournamentFormatId': tournamentFormatId})

    eventStates = tournamentState['eventState']['items']
    for eventState in eventStates:
        e = getEventState(eventState['id'])
        if e == None:
            return returnResponse(500, {'message': 'eventState does not exist in db', 'eventStateId': eventState['id'], 'tournamentStateId': tournamentState['id']})
        # call completeEventLambda
        completeEventEvent = {
            'body': {
                'eventStateId': eventState['id'],
                'tournamentStateId': tournamentState['id'],
            }
        }
        completeEventResponse = lambda_client.invoke(FunctionName='TournamentManagementStack-completeEventHandler63EA-sFnbq48soJki',
                                                     InvocationType='RequestResponse',
                                                     Payload=json.dumps(completeEventEvent))
        completeEventPayload = json.loads(
            completeEventResponse['Payload'].read())
        logger.debug('[completeEventPayload] {}'.format(completeEventPayload))
        if (completeEventPayload['statusCode'] < 200 or completeEventPayload['statusCode'] >= 300):
            logger.error('[completeTournamentHandler] Unable to complete event: {}'.format(
                eventState['id']))
            logger.error('[completeTournamentHandler] Response: {}'.format(
                completeEventResponse))
            return returnResponse(completeEventPayload['statusCode'], {'message': completeEventPayload['body'], 'eventStateId': eventState['id']})

    # set venue rooms as inactive
    venue = getVenue(tournamentFormat['venueId'])
    rooms = venue['rooms']
    if (len(rooms) == 0):
        logger.error(
            '[completeTournamentHandler] invalid venue rooms: %s', venue.get('id'))
        return returnResponse(500, {'message': 'Venue[rooms] is NULL', 'venueId': venue['id']})

    # set room statuses to inactive until event starts
    for room in rooms:

        judges = []
        competitors = []
        room_ = getRoom(room)
        updateRoom(room, 'INACTIVE', room_['_version'], judges, competitors)

    return returnResponse(200, {'message': 'tournament completed', 'tournamentFormatId': tournamentFormat['id'], 'roomIds': rooms, 'venueId': venue['id'], 'competitorEntries': competitorEntries, 'judgeIds': tournamentFormat['judges']})


def startEventHandler(event, context):
    printEvent(event, 'startEventHandler')
    printContext(context, 'startEventHandler')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    missingQueries = ''
    if body.get('tournamentStateId') == None:
        missingQueries += 'Requires tournamentStateId. '
    if body.get('eventFormatId') == None:
        missingQueries += 'Requires eventFormatId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    tournamentStateId = body['tournamentStateId']
    eventFormatId = body['eventFormatId']

    # single call for all rounds
    startRoundEvent = {
        'body': {
            'eventFormatId': eventFormatId,
            'tournamentStateId': tournamentStateId,
        },
        'path': '/start_rounds',
    }
    startRoundResponse = lambda_client.invoke(FunctionName='teems-round-manager',
                                              InvocationType='RequestResponse',
                                              Payload=json.dumps(startRoundEvent))
    payload = startRoundResponse['Payload']
    payload = json.loads(payload.read())
    logger.debug('[startEventHandler] payload: {}'.format(payload))

    if (payload.get('statusCode') == None):
        return returnResponse(200, {'message': 'event started', 'eventForamtId': eventFormatId})

    if (payload['statusCode'] < 200 or payload['statusCode'] >= 300):
        return returnResponse(payload['statusCode'], {'message': payload['body'], 'roundStateId': 'tmp', 'tournamentStateId': tournamentStateId, 'eventFormatId': eventFormatId})

    return returnResponse(200, {'message': 'event started', 'eventFormatId': eventFormatId})


# complete an event by completing all rounds
def completeEventHandler(event, context):
    printEvent(event, 'completeEventHandler')
    printContext(context, 'completeEventHandler')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    missingQueries = ''
    if body.get('tournamentStateId') == None:
        missingQueries += 'Requires tournamentStateId. '
    if body.get('eventFormatId') == None:
        missingQueries += 'Requires eventFormatId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    tournamentStateId = body['tournamentStateId']
    eventStateId = body['eventStateId']

    eventState = getEventState(eventStateId)
    roundStates = eventState['roundState']['items']

    for round in roundStates:
        completeRoundEvent = {
            'body': {
                'roundStateId': round['id'],
                'tournamentStateId': tournamentStateId,
                'eventStateId': eventStateId,
            },
            'path': '/complete_round',
        }
        completeRoundResponse = lambda_client.invoke(FunctionName='teems-round-manager',
                                                     InvocationType='RequestResponse',
                                                     Payload=json.dumps(completeRoundEvent))
        payload = completeRoundResponse['Payload']
        payload = json.loads(payload.read())
        logger.debug('[completeRoundPayload] payload: {}'.format(payload))
        if (payload['statusCode'] < 200 or payload['statusCode'] >= 300):
            return returnResponse(payload['statusCode'], {'message': payload['body'], 'roundStateId': round['id'], 'tournamentStateId': tournamentStateId, 'eventStateId': eventStateId})

    return returnResponse(200, {'message': 'event complete', 'eventStateId': eventStateId, 'tournamentStateId': tournamentStateId})


# start a room
def startRoomHandler(event, context):
    printEvent(event, 'startRoomHandler')
    printContext(event, 'startRoomHandler')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    missingQueries = ''
    if body.get('roomId') == None:
        missingQueries += 'Requires roomId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    roomId = body['roomId']
    room = getRoom(roomId)

    judges = room['judges']

    for judge in judges:
        judge_ = getJudge(judge['id'])

        if (judge_ == None):
            logger.error(
                '[startRoomHandler] invalid judge id: {}'.format(judge['id']))
            return returnResponse(400, {'message': 'invalid judge id', 'judgeId': judge['id']})

    if (room.get('status') == 'ACTIVE'):
        logger.error(
            '[startRoomHandler] room is already inactive: roomId {}'.format(roomId))
        return returnResponse(400, {'message': 'room is already inactive', 'roomId': roomId})

    updateRoomStatus(room['id'], 'ACTIVE', room['_version'])
    judgeIds = []
    for judge in judges:
        updateJudge(judge['id'], 'ACTIVE', judge['_version'])
        judgeIds.append(judge['id'])

    # not sure if we should do this here or in rounds
    competitorEntryIds = []
    for competitorEntry in room['competitorEntryIds']:
        competitorEntry_ = getCompetitorEntry(competitorEntry)
        updateCompetitorEntry(competitorEntry, 'ACTIVE',
                              competitorEntry_['_version'])
        competitorEntryIds.append(competitorEntry_['id'])

    return returnResponse(200, {'message': 'room start', 'roomId': roomId, 'judgeIds': judgeIds, 'competitorEntryIds': competitorEntryIds})

# complete a room


def completeRoomHandler(event, context):
    printEvent(event, 'completeRoomHandler')
    printContext(event, 'completeRoomHandler')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    missingQueries = ''
    if body.get('roomId') == None:
        missingQueries += 'Requires roomId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    roomId = body['roomId']

    room = getRoom(roomId)

    judges = room['judges']

    for judge in judges:
        judge_ = getJudge(judge['id'])

        if (judge_ == None):
            logger.error(
                '[completeRoomHandler] invalid judge id: {}'.format(judge['id']))
            return returnResponse(400, {'message': 'invalid judge id', 'judgeId': judge['id']})

    if (room.get('status') == 'INACTIVE'):
        logger.error(
            '[completeRoomHandler] room is already inactive: roomId {}'.format(roomId))
        return returnResponse(400, {'message': 'room is already inactive', 'roomId': roomId})

    updateRoomStatus(room['id'], 'INACTIVE', room['_version'])
    judgeIds = []
    for judge in judges:
        judge_ = getJudge(judge['id'])
        updateJudge(judge_['id'], 'INACTIVE', judge_['_version'])
        judgeIds.append(judge_['id'])

    competitorEntryIds = []
    for competitorEntry in room['competitorEntryIds']:
        competitorEntry_ = getCompetitorEntry(competitorEntry)
        updateCompetitorEntry(competitorEntry, "INACTIVE",
                              competitorEntry_['_version'])
        competitorEntryIds.append(competitorEntry)

    return returnResponse(200, {'message': 'room complete', 'judgeIds': judgeIds, 'competitorEntryIds': competitorEntryIds})


def freeJudgeHandler(event, context):
    printEvent(event, 'freeJudgeHandler')
    printContext(event, 'freeJudgeHandler')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    missingQueries = ''
    if body.get('tournamentFormatId') == None:
        missingQueries += 'Requires tournamentFormatId. '
    if body.get('judgeId') == None:
        missingQueries += 'Requires judgeId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    tournamentFormatId = body['tournamentFormatId']
    judgeId = event['body']['judgeId']

    print(formatGraphQuery('TournamentFormat', tournamentFormatId, [
          '_version', 'competitorEntryIds', 'judges', 'id', 'venueId', 'eventFee', 'eventFormatIds']))

    tournamentFormat = getTournamentFormat(tournamentFormatId)
    if tournamentFormat == None:
        return returnResponse(400, {'message': 'invalid tournamentFormatId', 'tournamentFormatId': tournamentFormatId})

    logger.debug(
        '[freeJudgeHandler] tournamentFormat: {}'.format(tournamentFormat))

    tournamentState = getTournamentState(
        tournamentFormat['tournamentState']['id'])
    judges = json.loads(tournamentState['judges'])

    logger.debug(
        '[freeJudgeHandler] tournamentState: {}'.format(tournamentState))

    if len(judges) == 0:
        return returnResponse(400, {'message': 'no judges int tournamentState', 'tournamentFormatId': tournamentFormatId, 'tournamentStateId': tournamentState['id']})

    while (type(judges) == str):
        judges = json.loads(judges)

    print(judges)
    # set judge as inactive
    for judge in judges:
        if judge['judgeId'] == judgeId:
            judge_ = getJudge(judgeId)
            if judge_ == None:
                return returnResponse(400, {'message': 'invalid judge', 'judgeId': judge})
            print('checking assignment')
            if judge['assigned'] != True:
                return returnResponse(400, {'message': 'judge is already inactive', 'judgeId': judge})
            judge['assigned'] = False

    logger.debug('[freeJudgeHandler] judges: {}'.format(judges))
    print(judges)

    tournamentState['judges'] = judges

    if (updateTournamentState(tournamentState, tournamentState['_version']) == False):
        return returnResponse(500, {'message': 'issue updating tournament state', 'tournamentState': tournamentState})

    return returnResponse(200, {'message': 'judge inactive', 'judgeId': judgeId, 'tournamentFormatId': tournamentFormatId})


def useJudgeHandler(event, context):
    printEvent(event, 'useJudgeHandler')
    printContext(event, 'useJudgeHandler')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    missingQueries = ''
    if body.get('tournamentFormatId') == None:
        missingQueries += 'Requires tournamentFormatId. '
    if body.get('judgeId') == None:
        missingQueries += 'Requires judgeId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    tournamentFormatId = body['tournamentFormatId']
    judgeId = event['body']['judgeId']

    print(formatGraphQuery('TournamentFormat', tournamentFormatId, [
          '_version', 'competitorEntryIds', 'judges', 'id', 'venueId', 'eventFee', 'eventFormatIds']))

    tournamentFormat = getTournamentFormat(tournamentFormatId)
    if tournamentFormat == None:
        return returnResponse(400, {'message': 'invalid tournamentFormatId', 'tournamentFormatId': tournamentFormatId})

    logger.debug(
        '[useJudgeHandler] tournamentFormat: {}'.format(tournamentFormat))

    tournamentState = getTournamentState(
        tournamentFormat['tournamentState']['id'])
    judges = json.loads(tournamentState['judges'])

    logger.debug(
        '[useJudgeHandler] tournamentState: {}'.format(tournamentState))

    if len(judges) == 0:
        return returnResponse(400, {'message': 'no judges int tournamentState', 'tournamentFormatId': tournamentFormatId, 'tournamentStateId': tournamentState['id']})

    while (type(judges) == str):
        judges = json.loads(judges)

    print(judges)
    # set judge as active
    for judge in judges:
        if judge['judgeId'] == judgeId:
            judge_ = getJudge(judgeId)
            if judge_ == None:
                return returnResponse(400, {'message': 'invalid judge', 'judgeId': judge})
            print('checking assignment')
            if judge['assigned'] == True:
                return returnResponse(400, {'message': 'judge is already active', 'judgeId': judge})
            judge['assigned'] = True

    logger.debug('[useJudgeHandler] judges: {}'.format(judges))
    tournamentState['judges'] = judges

    if (updateTournamentState(tournamentState, tournamentState['_version']) == False):
        return returnResponse(500, {'message': 'issue updating tournament state', 'tournamentState': tournamentState})

    return returnResponse(200, {'message': 'judge active', 'judgeId': judgeId, 'tournamentFormatId': tournamentFormatId})


def getAvailableJudgesHandler(event, context):
    printContext(context, 'getAvailableJudges')
    printEvent(event, 'getAvailableJudges')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    missingQueries = ''
    if body.get('tournamentStateId') == None:
        missingQueries += 'Requires tournamentStateId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    tournamentStateId = body['tournamentStateId']
    tournamentState = getTournamentState(tournamentStateId)
    if tournamentState == None:
        return returnResponse(400, {'message': 'Invalid tournamentStateId input', 'tournamentStateId': tournamentStateId})

    availableJudges = []
    availableJudges = getAvailableJudge(tournamentStateId, -1)

    return returnResponse(200, {'message': 'Available judges', 'judgeIds': availableJudges})


def getAvailableRoomsHandler(event, context):
    printContext(context, 'getAvailableRooms')
    printEvent(event, 'getAvailableRooms')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    missingQueries = ''
    if body.get('tournamentFormatId') == None:
        missingQueries += 'Requires tournamentFormatId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    tournamentFormatId = body['tournamentFormatId']
    tournamentFormat = getTournamentFormat(tournamentFormatId)

    if (tournamentFormat == None):
        return returnResponse(400, {'message': 'invalid tournamentFormatId', 'tournamentForamtId': tournamentFormatId})

    logger.debug(
        '[getAvailableRoomsHandler] tournamentFormat: {}'.format(tournamentFormat))

    venue = getVenue(tournamentFormat['venueId'])
    if (venue == None):
        logger.error(
            '[getAvailableRoomsHandler] venue does not exist in tournamentFormat: %s', tournamentFormatId)
        return returnResponse(500, {'message': 'tournamentFormat does not have a venue', 'tournamentFormatId': tournamentFormatId})

    logger.debug('[getAvailableRoomsHandler] venue: {}'.format(venue))

    rooms = getAvailableRooms(venue['id'])

    return returnResponse(200, {'message': 'Available rooms', 'roomIds': rooms})


def getEventCompetitorsHandler(event, context):
    printContext(context, 'getEventCompetitor')
    printEvent(event, 'getEventCompetitor')

    body = event['body']
    if type(body) == str:
        body = json.loads(event['body'])

    logger.debug('[getEventCompetitor] body: {}'.format(body))

    missingQueries = ''
    if body.get('tournamentFormatId') == None:
        missingQueries += 'Requires tournamentFormatId. '
    if body.get('eventFormatId') == None:
        missingQueries += 'Requires eventFormatId. '
    if missingQueries != '':
        return returnResponse(400, {'message': 'query is invalid. {msg}'})

    eventFormatId = body['eventFormatId']
    tournamentFormatId = body['tournamentFormatId']

    tournamentFormat = getTournamentFormat(tournamentFormatId)
    if tournamentFormat == None:
        return returnResponse(400, {"message": "tournamentFormat does not exist", "tournamentFormatId": tournamentFormatId})

    eventFormat = None
    if eventFormatId in tournamentFormat['eventFormatIds']:
        eventFormat = getEventFormat(eventFormatId)
    if eventFormat == None:
        return returnResponse(400, {'message': 'eventFormatId is not a part of the provided tournamentFormatId', 'tournamentFormatId': tournamentFormatId, 'eventFormatId': eventFormatId})

    competitorEntries = getEventCompetitors(tournamentFormatId, eventFormatId)

    return returnResponse(200, {'message': 'Competitor entries found', 'competitorIds': competitorEntries, 'eventIds': eventFormatId})
