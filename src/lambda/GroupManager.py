from constants.Response import returnResponse
from classes.RoundState import RoundState
from classes.Group import Group
from classes.EventState import EventState
from classes.EventFormat import EventFormat
from aws_helper.AppSyncQuery import AppSync_query
from collections import deque
from LambdaHelper import LambdaHelper
import boto3
import random
import json
import logging
import os
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
    
def startGroups_handler(event, context):
    """_summary_

    This function takes groups from the queued and assigns them to rooms.
    1, Check and Carry out groups from queued.
        1.1, the number of groups <= the number of available rooms && <= the number of Judges
    2, Call tournamentManager.getAvailableRooms() to get available rooms.
    3, Call tournamentManager.getAvailableJudges() to get available judges.
        3.1 Get judgesPerRound in eventFormat by using the currentRoundIdx in EventState
    4, Call tournamentManager.useJudge() to assign judges to groups
    5, Call tournamentManager.startRoom() to occupy rooms with groups.
    6, Move the groups to assigned.
    7, Batch processing update the roundState

    """
    logger.info("********** Start startGroups service **********")
    logger.debug('event:{}'.format(json.dumps(event)))

    secret_name = os.environ["secretName"]
    region = os.environ["region"]
    
    if type(event["body"]) == str:
        event["body"] = json.loads(event["body"])
    
    if "roundStateId" not in event["body"]:
        return returnResponse(400, {"message": "Invalid input, missing `roundStateId` in the request"})

    appsyncy_query = AppSync_query(secret_name, region)
    lambda_helper = LambdaHelper()
    
    roundStateId = event["body"]["roundStateId"]
    logger.debug("********** Here is the roundstateId **********" + roundStateId)
    
    roundStateObj, eventStateObj, eventFormatObj, tournamentFormatId, tournamentStateId, tournamentStateInfo = lambda_helper.retrive_appsync(appsyncy_query, roundStateId)

    currentRoundIdx = eventStateObj.get_currentRoundIdx()

    rounds = eventFormatObj.get_rounds()
    
    logger.debug("********** rounds in eventFormat **********")
    logger.debug(rounds)

    # 1.
    group_list = []
    queued_list = roundStateObj.get_queued()
    try:
        for queued_group_info in queued_list:
            cur_group = Group(json.loads(queued_group_info))
            group_list.append(cur_group)
    except Exception as err:
        logger.debug("********** Error happened in loop queued_list **********")
        logger.debug(str(err))
        return returnResponse(500, {"message": "Error happened, because {}".format(str(err))})
    if not group_list:
        return returnResponse(400, {"message": "No group in queued"})
    
    # 2, 3
    available_judges_list, available_rooms_list,  og_judges_list, og_rooms_list = lambda_helper.get_availableJudgesRooms(tournamentStateInfo)
    
    if not available_judges_list or not available_rooms_list:
        return returnResponse(400, {"message" :  "Please check log, No judgeIds/roomIds in the tournamentState {}".format(tournamentStateId)})
    
    total_room = len(available_rooms_list)
    total_judges = len(available_judges_list)
    
    logger.debug("********** og_rooms_list **********")
    logger.debug(og_rooms_list)
    logger.debug("********** og_judges_list **********")
    logger.debug(og_judges_list)
    logger.debug("********** available_rooms_list  **********")
    logger.debug(available_rooms_list)
    logger.debug("length of room_list is {}".format(total_room))
    logger.debug("********** available_judges_list **********")
    logger.debug(available_judges_list)
    logger.debug("length of available_judges_list is {}".format(total_judges))

    if total_room == 0:
        return returnResponse(400, {"message" : "Sorry, No rooms available at this time"})
    if total_judges == 0:
        return returnResponse(400, {"message" : "Sorry, No judges available at this time"})
    
    # randomly shuffle the group and jusdges list
    random.shuffle(group_list)
    random.shuffle(available_judges_list)

    # Get the number of jusges needed per round
    judges_need = lambda_helper.get_judges_need(rounds, currentRoundIdx)

    # arrang_judges_list stores arranged judges
    arrang_judges_list = lambda_helper.get_arrange_judges(judges_need, total_judges, available_judges_list)
    
    # 4,5,6
    deq_group = deque(group_list)
    try:
        lambda_helper.group_assign_group_judge(appsyncy_query, deq_group, arrang_judges_list, available_rooms_list, roundStateObj, og_judges_list, og_rooms_list, tournamentStateInfo)
    except Exception as err:
        logger.debug(
                    "Error happened in lambda_helper.group_assign_group_judge, because {}".format(str(err)))
        return returnResponse(400, {"message": "Error happened in lambda_helper.group_assign_group_judge, because {}".format(str(err))})
    
    # 7. Batch update
    try:
        appsyncy_query.updateRoundState_queued_assigned_query(
            roundStateObj.get_round_info())
    except Exception as err:
        logger.debug("Batch update issuse" + str(err))
        return returnResponse(400, {"message": "Error happened in Batch update, because {}".format(str(err))})

    return returnResponse(200, {"message": "{} groups are in the waiting list".format(len(deq_group))})


def startCompetition_handler(event, context):
    """_summary_

    Judges will call this function to start the competition.
    1, Place the group from assigned into started

    """

    logger.info("**** Start startCompetition service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    secret_name = os.environ["secretName"]
    region = os.environ["region"]
    if type(event["body"]) == str:
        event["body"] = json.loads(event["body"])
    if "roundStateId" not in event["body"]:
        return returnResponse(400, {"message": "Invalid input, missing `roundStateId` in the request"})
    if "groupId" not in event["body"]:
        return returnResponse(400, {"message": "Invalid input, missing `groupId` in the request"})

    roundStateId = event["body"]["roundStateId"]
    groupId = event["body"]["groupId"]
    
    logger.debug("********** roundStateId **********")
    logger.debug(roundStateId)
    logger.debug("********** groupId **********")
    logger.debug(groupId)
    
    appsyncy_query = AppSync_query(secret_name, region)
    try:
        roundStateInfo = appsyncy_query.getRoundState_query(roundStateId)
    except Exception as err:
        logger.debug(str(err))
        return returnResponse(400, {"message": "Error happened in retreving round state, because {}".format(err)})
    roundStateObj = RoundState(roundStateInfo)
    logger.debug("********** roundStateObj **********")
    logger.debug(str(roundStateObj.get_round_info()))
    
    assigned_list = roundStateObj.get_assigned()
    logger.debug("********** Assigned List **********")
    logger.debug(assigned_list)
    
    try:
        for group_info in assigned_list:
            group = Group(json.loads(group_info))
            if groupId == group.get_id():
                # 1.
                # update local
                roundStateObj.assigned_to_started(group.get_group_json())
                break
        # update to DB
        appsyncy_query.updateRoundState_assigned_started_query(
            roundStateObj.get_round_info())
    except Exception as e:
        logger.debug(str(e))
        return returnResponse(500, {"message": "Error happened, because {}".format(e)})
    return returnResponse(200, roundStateObj._version)


def collectResult_handler(event, context):
    """_summary_

    This function will be called when a round is completed and used to collect judging results from the completed round.
    1, Saving the judging result in roundState Obj in local.
    2, Call tournamentManager.freeJudge() to free judges
    3, Release the occupied room by calling tournamentManager.finishRoom(roomId, adminId)
    4, First update result to DB
    5, queued is not empty
        5.1 take A group from queue to assigned locally
    6, assigned is not empty: 
            Call startRoom(eventId, roomId, adminId) to strat the room.
            Second update result to DB
    7, if all completed,Call roundManager.completeRound(roundId) to pass the control to roundManager. 
        else, return
    """
    logger.info("**** Start collectResult service --->")
    logger.debug('event:{}'.format(json.dumps(event)))
    secret_name = os.environ["secretName"]
    region = os.environ["region"]
    
    if type(event["body"]) == str:
        event["body"] = json.loads(event["body"])
    
    if "roundStateId" not in event["body"]:
        return returnResponse(400, {"message": "Invalid input, missing `roundStateId` in the request"})
    if "groupId" not in event["body"]:
        return returnResponse(400, {"message": "Invalid input, missing `groupId` in the request"})
    if "ranking" not in event["body"]:
        return returnResponse(400, {"message": "Invalid input, missing `ranking` in the request"})

    roundStateId = event["body"]["roundStateId"]
    groupId = event["body"]["groupId"]
    ranking = event["body"]["ranking"]

    lambda_client = boto3.client('lambda', region_name="us-east-1")

    appsyncy_query = AppSync_query(secret_name, region)
    lambda_helper = LambdaHelper()
    
    roundStateObj, eventStateObj, eventFormatObj, tournamentFormatId, tournamentStateId, tournamentStateInfo = lambda_helper.retrive_appsync(appsyncy_query, roundStateId)
    eventFormatId = roundStateObj.get_eventFormatId()
    eventStateId = roundStateObj.get_eventStateId()
    judgeIds = []
    roomId = ""
    
    started_list = roundStateObj.get_started()
    logger.debug("********** started list in roundState **********")
    logger.debug(started_list)
    
    if started_list:
        try:
            # 1.  save result in local
            for started_info in started_list:
                group = Group(json.loads(started_info))
                if groupId == group.get_id():
                    judgeIds = group.get_judges()
                    roomId = group.get_roomId()
                    group.set_ranking(ranking)
                    roundStateObj.started_to_completed(group.get_group_json())
                    break
            
            # 2. release judges
            tournamentStateInfo['judges']=lambda_helper.release_judge(json.loads(tournamentStateInfo['judges']), judgeIds)

            # 3. release rooms
            tournamentStateInfo['rooms']=lambda_helper.release_room(json.loads(tournamentStateInfo['rooms']), roomId)
        
            # 4. First update result in DB
            logger.debug("********** 1 update roundState **********")
            logger.debug(str(roundStateObj.get_round_info()))
            appsyncy_query.updateRoundState_udpate_all_groups_query(roundStateObj.get_round_info())
            roundStateObj.update_version()
            
            # batch update the TournamentState
            logger.debug("********** update tounrnamentState if started_list **********")
            logger.debug(tournamentStateInfo)
            appsyncy_query.update_judges_rooms_TournamentState_query(tournamentStateInfo['id'],tournamentStateInfo['_version'], tournamentStateInfo['judges'], tournamentStateInfo['rooms'])
            tournamentStateInfo['_version'] += 1
            
            # 5. 
            ququed_list = roundStateObj.get_queued()
            logger.debug("********** ququed list in roundState **********")
            logger.debug(ququed_list)
            if ququed_list:
                picked_group = Group(json.loads(random.choice(ququed_list)))
                picked_group.set_judges(judgeIds)
                picked_group.set_roomId(roomId)
                roundStateObj.queued_to_assigned(picked_group.get_group_json())
        except Exception as err:
            logger.debug("********** Exception in started_list **********")
            logger.debug(str(err))
            return returnResponse(500, {"message":"Error happnes, becuase {}".format(str(err))})
    # 6. 
    assigned_list = roundStateObj.get_assigned()
    logger.debug("********** assigned list in roundState **********")
    logger.debug(assigned_list)

    if assigned_list:
        group = Group(json.loads(assigned_list[0]))
        next_group_id = group.get_id()
        if not group.get_roomId():
            try:
                tournamentStateInfo['rooms'] = lambda_helper.use_room(json.loads(tournamentStateInfo['rooms']), roomId)
                
            except Exception as e:
                logger.debug(
                    "Assign room to the next group id {} failed, reason: {}".format(next_group_id, str(e)))
                return returnResponse(400, {"message": "Error happened in moveing assigned group to started, {}".format(e)})
            
            group.set_roomId(roomId)

        if not group.get_judges():
            try:
                tournamentStateInfo['judges'] = lambda_helper.use_judge(json.loads(tournamentStateInfo['judges']), judgeIds)
                
            except Exception as e:
                logger.debug(
                    "Assign judges to the next group id {} failed, reason: {}".format(next_group_id, str(e)))
                return returnResponse(400, {"message": "Error happened in moveing assigned group to started, {}".format(e)})

            group.set_judges(judgeIds)
            
        else:
            tournamentStateInfo['rooms'] = lambda_helper.use_room(json.loads(tournamentStateInfo['rooms']), group.get_roomId())
            tournamentStateInfo['judges'] = lambda_helper.use_judge(json.loads(tournamentStateInfo['judges']), group.get_judges())
    
        roundStateObj.assigned_to_started(group.get_group_json())
        
        # batch update the TournamentState
        logger.debug("********** update tounrnamentState if assigned_list **********")
        logger.debug(tournamentStateInfo)
        appsyncy_query.update_judges_rooms_TournamentState_query(tournamentStateInfo['id'],tournamentStateInfo['_version'], json.dumps(tournamentStateInfo['judges']), json.dumps(tournamentStateInfo['rooms']))
        tournamentStateInfo['_version'] += 1
            
    logger.debug("********** 2 Updated roundState **********")
    logger.debug(str(roundStateObj.get_round_info()))
    appsyncy_query.updateRoundState_udpate_all_groups_query(roundStateObj.get_round_info())
    
    # 7
    if roundStateObj.all_completed():
        lambda_helper.complete_round(lambda_client, roundStateId)
        tournamentStateInfo['judges'] = lambda_helper.release_all_judges(json.loads(tournamentStateInfo['judges']))
        tournamentStateInfo['rooms'] = lambda_helper.release_all_rooms(json.loads(tournamentStateInfo['rooms']))
        logger.debug("********** all groups completed, judges and rooms are **********")
        logger.debug(tournamentStateInfo['judges'])
        logger.debug( tournamentStateInfo['rooms'])
        # batch update the TournamentState
        logger.debug("********** update tounrnamentState if all_completed **********")
        logger.debug(tournamentStateInfo)
        appsyncy_query.update_judges_rooms_TournamentState_query(tournamentStateInfo['id'],tournamentStateInfo['_version'], tournamentStateInfo['judges'], tournamentStateInfo['rooms'])
         
        return returnResponse(200, {"message": "all groups are completed"})
    else:
        return returnResponse(200, {"message": "some groups are still in progress"})
