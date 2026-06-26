import logging
import boto3
import json
import os
import random
from constants.Response import returnResponse
from constants.CommonPrints import printContext, printEvent
from aws_helper.DynamoDB import update_item_db, scan_items_db, put_item_db
from aws_helper.appsync import query
from gql import gql
from dotenv import load_dotenv


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def removeWhiteSpace(text: str):
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    return text

def formatGraphQuery(function: str, id: str, requests: list):
    myQuery = """
query MyQuery {
get%s(id: %s) {
%s
}
}
    """
    data = ' \n'.join(requests)
    myQuery = myQuery % (function, '"' + id + '"', data)
    return myQuery

def getTournamentFormat(tournamentId: str):
    myQuery = """
query MyQuery {
getTournamentFormat(id: %s) {
_version 
id 
_deleted 
_lastChangedAt 
createdAt 
description 
eventFee 
eventFormatIds 
name 
owner 
startTime 
tournamentFormatTournamentStateId 
updatedAt 
venueId 
tournamentState { 
id 
} 
judges { 
items { 
id 
judgeID 
} 
} 
competitionEntries { 
items { 
id 
}
}
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + tournamentId + '"')
    print(myQuery)
    tournamentFormat = query(myQuery, {})
    print(tournamentFormat)
    if tournamentFormat == None:
        return None

    tournamentFormat = tournamentFormat['getTournamentFormat']
    return tournamentFormat

def getTournamentState(tournamentId: str):
    myQuery = """
query MyQuery {
getTournamentState(id: %s) {
_deleted 
_lastChangedAt 
_version 
competitors 
createdAt 
eventFormatIds 
id 
judges 
tournamentFormatId 
updatedAt 
eventState {
items {
id 
}
}
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + tournamentId + '"')
    print(myQuery)
    tournamentState = query(myQuery, {})
    print(tournamentState)
    if tournamentState == None:
        return None

    tournamentState = tournamentState['getTournamentState']
    return tournamentState

def getEventState(eventStateId: str):
    myQuery = """
query MyQuery {
getEventState(id: %s) {
updatedAt 
tournamentStateId 
tournamentFormatId 
roundState { 
items { 
id 
} 
} 
id 
eventFormatId 
currentRoundIdx 
createdAt 
awards 
_version 
_lastChangedAt 
_deleted 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + eventStateId + '"')

    eventState = query(myQuery, {})
    if eventState == None:
        return None
    eventState = eventState['getEventState']
    return eventState

def getEventFormat(eventFormatId: str):
    myQuery = """
query MyQuery($id: ID = %s) {
getEventFormat(id: $id) {
_deleted 
_lastChangedAt 
_version 
awards 
createdAt 
id 
name 
owner 
rounds 
updatedAt 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + eventFormatId + '"')

    eventFormat = query(myQuery, {})
    if eventFormat == None:
        return None
    eventFormat = eventFormat['getEventFormat']
    return eventFormat

def getJudge(judgeId: str):
    myQuery = """
query MyQuery($id: ID = %s) {
getJudge(id: $id) {
_deleted 
_lastChangedAt 
_version 
createdAt 
id 
updatedAt 
name 
tournamentFormats { 
items { 
id 
}
}
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + judgeId + '"')

    judge = query(myQuery, {})
    if judge == None:
        return None
    judge = judge['getJudge']
    return judge

def getAvailableJudge(tournamentStateId: str, numberOfJudges: int):
    judges = []
    tournamentState = getTournamentState(tournamentStateId)
    if tournamentState == None:
        return None
    judges_ = json.loads(tournamentState['judges'])
    logger.debug("[getAvailableJudge] judges: {}".format(judges_))
    logger.debug("[getAvailableJudge] judgesType: {}".format(type(judges_)))
    while type(judges_) == str:
        judges_ = json.loads(judges_)
    logger.debug("[getAvailableJudge] judges: {}".format(judges_))
    i = 0
    for judge in judges_:
        print(judge)
        if (i == numberOfJudges):
            break
        judge_ = getJudge(judge['judgeId'])
        print('judge: {}'.format(judge_))
        if judge_ != None:
            if judge['assigned'] == False:
                judges.append(judge)
                i+=1
    return judges

def getCompetitor(competitorId: str):
    myQuery = """
query MyQuery($id: ID = %s) {
getCompetitor(id: $id) {
_deleted 
_lastChangedAt 
_version 
competitorentryID 
createdAt 
id 
status 
updatedAt 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + competitorId + '"')

    competitor = query(myQuery, {})
    if competitor == None:
        return None
    competitor = competitor['getCompetitor']
    return competitor

def getCompetitorEntry(competitorEntryId: str):
    myQuery = """
query MyQuery($id: ID = %s) {
getCompetitorEntry(id: $id) {
_deleted 
_lastChangedAt 
_version 
competitors { 
items { 
id 
} 
} 
createdAt 
id 
updatedAt 
eventFormatIds 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + competitorEntryId + '"')

    competitorEntry = query(myQuery, {})
    if competitorEntry == None:
        return None
    competitorEntry = competitorEntry['getCompetitorEntry']
    return competitorEntry

def getAvailableCompetitorEntries(tournamentId: str, numberOfEntries: int):
    entries = []
    tournamentFormat = getTournamentFormat(tournamentId)
    i = 0
    for entry in tournamentFormat['competitorEntryIds']:
        if (i == numberOfEntries):
            break
        entry_ = getCompetitorEntry(entry)
        if entry_ != None:
            if entry_['status'] == 'INACTIVE':
                entries.append(entry)
                i+=1
    return entries

def getRoom(roomId: str):
    myQuery = """
query MyQuery($id: ID = %s) {
getRoom(id: $id) {
_deleted 
_lastChangedAt 
_version 
competitorEntryIds 
createdAt 
id 
judges 
status 
venueId 
updatedAt 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + roomId + '"')

    room = query(myQuery, {})
    if room == None:
        return None
    room = room['getRoom']
    return room

def getAvailableRooms(venueId: str):
    rooms = []
    venue = getVenue(venueId)
    for room in venue['rooms']:
        r = getRoom(room)
        if r != None:
            rooms.append(r['id'])
    return rooms

def getVenue(venueId: str):
    myQuery = """
query MyQuery($id: ID = %s) {
getVenue(id: $id) {
venueType 
updatedAt 
rooms 
owner 
name 
id 
createdAt 
address 
_version 
_lastChangedAt 
_deleted 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    myQuery = myQuery % ('"' + venueId + '"')

    venue = query(myQuery, {})
    if venue == None:
        return None
    venue = venue['getVenue']
    return venue

def updateJudge(judge: str, status: str, version: int):
    myQuery = """
mutation MyMutation($status: String, $id: ID!, $_version: Int) {
  updateJudge(input: {_version: $_version, id: $id, status: $status}) {
    id
    status
    _version
  }
}
    """
    myQuery = removeWhiteSpace(myQuery)
    variables = {
        '_version': version,
        'status': status,
        'id': judge,
    }
    judge = query(myQuery, variables)
    if judge != None:
        return True
    return False

def updateCompetitor(competitor: str, status: str, version: int):
    myQuery = """
mutation MyMutation($_version: Int, $id: ID!, $status: String) {
updateCompetitor(input: {status: $status, id: $id, _version: $_version}) {
_deleted
_lastChangedAt
_version
competitorentryID
createdAt
id
status
updatedAt
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    variables = {
        '_version': version,
        'id': competitor,
        'status': status,
    }
    competitor = query(myQuery, variables)
    if competitor != None:
        return True
    return False

def updateCompetitorEntry(competitorEntry: dict, version: int):
    myQuery = """
mutation MyMutation($_version: Int, $id: ID!, $tournamentFormatId: ID!) {
updateCompetitorEntry(input: {_version: $_version, id: $id, tournamentFormatId: $tournamentFormatId}) {
_deleted 
_lastChangedAt 
_version 
competitors { 
items { 
id  
competitorID 
competitorEntryID 
} 
} 
updatedAt 
tournamentFormatId 
id 
createdAt 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    variables = {
        '_version': version,
        'id': competitorEntry['id'],
        'tournamentFormatId': competitorEntry['tournamentFormatId']
    }
    competitorEntry = query(myQuery, variables)
    if competitorEntry != None:
        return True
    return False

def updateRoomStatus(roomId: str, status: str, version: int):
    myQuery = """
mutation MyMutation($status: String, $id: ID!, $_version: Int ) {
  updateRoom(input: {_version: $_version, id: $id, status: $status}) {
venueId 
updatedAt 
status 
judges 
id 
createdAt 
competitorEntryIds 
_version 
_lastChangedAt 
_deleted 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    variables = {
        '_version': version,
        'status': status,
        'id': roomId,
    }
    room = query(myQuery, variables)
    if room != None:
        return True
    return False

def updateRoom(roomId: str, status: str, version: int, judges: list, competitorEntryIds: list):
    myQuery = """
mutation MyMutation($_version: Int, $competitorEntryIds: [String], $id: ID!, $judges: [String], $status: String) {
updateRoom(input: {_version: $_version, competitorEntryIds: $competitorEntryIds, judges: $judges, status: $status, id: $id}) {
_deleted 
_lastChangedAt 
_version 
competitorEntryIds 
createdAt 
id 
judges 
status 
updatedAt 
venueId 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    variables = {
        '_version': version,
        'status': status,
        'id': roomId,
        'judges': judges,
        'competitorEntryIds': competitorEntryIds,
    }
    room = query(myQuery, variables)
    if room != None:
        return True
    return False

def updateTournamentState(tournamentState, version):
    myQuery = """
mutation MyMutation($judges: AWSJSON, $id: ID!, $eventFormatIds: [ID!], $competitors: AWSJSON, $_version: Int, $tournamentFormatId: ID!) {
updateTournamentState(input: {_version: $_version, competitors: $competitors, eventFormatIds: $eventFormatIds, id: $id, judges: $judges, tournamentFormatId: $tournamentFormatId}) {
updatedAt 
tournamentFormatId 
judges 
id 
eventFormatIds 
createdAt 
competitors 
_version 
_lastChangedAt 
_deleted 
}
}
"""
    myQuery = removeWhiteSpace(myQuery)
    if type(tournamentState['competitors'] != str):
        tournamentState['competitors'] = json.dumps(tournamentState['competitors'])
    if type(tournamentState['judges'] != str):
        tournamentState['judges'] = json.dumps(tournamentState['judges'])
    variables = {
        'id': tournamentState['id'],
        '_version': version,
        'judges': tournamentState['judges'],
        'eventFormatIds': tournamentState['eventFormatIds'],
        'competitors': tournamentState['competitors'],
        'tournamentFormatId': tournamentState['tournamentFormatId']
    }
    print()
    print('updateTournamentState')
    print(tournamentState)
    tournamentState = query(myQuery, variables)
    if tournamentState != None:
        return True
    return False

def updateTournamentFormat(tournamentFormat: dict, version: int):
    myQuery = """
mutation MyMutation($_version: Int, $description: String, $eventFee: Float, $eventFormatIds: [ID!], $id: ID!, $name: String, $startTime: AWSDateTime, $venueId: ID!, $tournamentFormatTournamentStateId: ID!) {
updateTournamentFormat(input: {_version: $_version, description: $description, eventFee: $eventFee, eventFormatIds: $eventFormatIds, id: $id, name: $name, startTime: $startTime, tournamentFormatTournamentStateId: $tournamentFormatTournamentStateId, venueId: $venueId}) {
_deleted 
_lastChangedAt 
_version 
createdAt 
description 
eventFee 
eventFormatIds 
id 
name 
owner 
startTime 
tournamentFormatTournamentStateId 
updatedAt 
venueId 
}
}
    """
    myQuery = removeWhiteSpace(myQuery)
    print()
    print('tournamentFormat')
    print(tournamentFormat)
    print()
    variables = {
        '_version': tournamentFormat['_version'],
        'description': tournamentFormat['description'],
        'eventFee': tournamentFormat['eventFee'],
        'eventFormatIds': tournamentFormat['eventFormatIds'],
        'id': tournamentFormat['id'],
        'name': tournamentFormat['name'],
        'startTime': tournamentFormat['startTime'],
        'venueId': tournamentFormat['venueId'],
        'tournamentFormatTournamentStateId': tournamentFormat['tournamentFormatTournamentStateId'],
    }
    tournamentFormat = query(myQuery, variables)
    if tournamentFormat != None:
        return True
    return False

def getEventCompetitors(tournamentFormatId, eventFormatId):
    myQuery = """
query MyQuery($id: ID!, $eq: ID!) {
  getTournamentFormat(id: $id) { 
    competitionEntries(filter: {eventFormatIds: {eq: $eq}}) { 
      items { 
        id 
      } 
    } 
  } 
} 
    """

    myQuery = removeWhiteSpace(myQuery)
    variables = {
        "id": tournamentFormatId,
        "eq": eventFormatId,
    }
    competitors = query(myQuery, variables)

    if competitors != None:
        return competitors['getTournamentFormat']['competitionEntries']['items']
    return False