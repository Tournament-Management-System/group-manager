from constants.Response import returnResponse
from classes.RoundState import RoundState
from classes.EventState import EventState
from classes.EventFormat import EventFormat
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

completeRoundHandler = 'arn:aws:lambda:us-east-1:695867875070:function:teems-round-manager'

class LambdaHelper():
    def retrive_appsync(self, appsyncy_query, roundStateId):
        
        """
        This function returns informations that are related to given round State Id.
        """
        
        roundStateInfo = appsyncy_query.getRoundState_query(roundStateId)
        logger.debug("roundStateInfo" + json.dumps(roundStateInfo))
        
        roundStateObj = RoundState(roundStateInfo)
        tournamentFormatId = roundStateObj.get_tournamentFormatId()
        tournamentStateId = roundStateObj.get_tournamentStateId()
        eventFormatId = roundStateObj.get_eventFormatId()
        eventStateId = roundStateObj.get_eventStateId()
        
        try:
            event_state_query = appsyncy_query.getEventState_query(eventStateId)
            event_format_query = appsyncy_query.getEventFormat_query(eventFormatId)
            tournamentStateInfo = appsyncy_query.getTournamentState_query(tournamentStateId)
            tournamentStateInfo = tournamentStateInfo['getTournamentState']
        except Exception as e:
            logger.debug("error in graphql, {}".format(str(e)))
            return returnResponse(400, {"message": "Error happened in graphql, {}".format(e)})
        
        eventStateObj = EventState(event_state_query)
        logger.debug("********** eventStateObj **********" )
        logger.debug(str(eventStateObj.get_eventEventState_info()))
        eventFormatObj = EventFormat(event_format_query)
        logger.debug("********** eventFormatObj **********")
        logger.debug(str(eventFormatObj.get_event_info()))
        logger.debug("********** tournamentFormatId **********")
        logger.debug(str(tournamentFormatId))
        logger.debug("********** tournamentStateId **********")
        logger.debug(str(tournamentStateId))
        logger.debug("********** tournamentStateInfo **********")
        logger.debug(str(tournamentStateInfo))
        return roundStateObj, eventStateObj, eventFormatObj, tournamentFormatId, tournamentStateId, tournamentStateInfo

    def use_judge(self, og_judges_list, use_judges_id):
        for judge_info in og_judges_list:
                if judge_info['judgeId'] in use_judges_id:
                    judge_info['assigned'] = True
        return og_judges_list
    
    def use_room(self, og_rooms_list, use_room_id):
        for room_info in og_rooms_list:
                if room_info['roomId'] == use_room_id:
                    room_info['available'] = False
        return og_rooms_list
    
    def release_judge(self,judge_infos, judgeIds):
        for judge_info in judge_infos:
            logger.debug("___ type of judge_info is {} ___".format(type(judge_info)))
            for judgeId in judgeIds:
                if judgeId == judge_info['judgeId']:
                    judge_info['assigned'] = False
        return json.dumps(judge_infos)
        

    def release_room(self, room_infos, roomId):
        if type(room_infos) == str:
            room_infos = json.loads(room_infos)
        logger.debug("=========== type of room_infos is {} ===========".format(type(room_infos)))
        logger.debug("===========room_info==========>")
        logger.debug(room_infos)
        for room_info in room_infos:
            if roomId == room_info['roomId']:
                room_info['available'] = True
        return json.dumps(room_infos)
    
    def release_all_judges(self, judge_infos):
        for judge_info in judge_infos:
            judge_info['assigned'] = False
        return json.dumps(judge_infos)
    
    def release_all_rooms(self, room_infos):
        for room_info in room_infos:
            room_info['available'] = True
        return json.dumps(room_infos)
    
    def get_availableJudgesRooms(self, tournamentStateInfo):
        available_judges_list = []
        available_rooms_list = []
        if tournamentStateInfo['judges'] == None or tournamentStateInfo['rooms'] == None:
            return available_judges_list, available_rooms_list, [], [] 
        judges_ = json.loads(tournamentStateInfo['judges'])
        rooms_ = json.loads(tournamentStateInfo['rooms'])
        
        while type(judges_) == str:
            judges_ = json.loads(judges_)
        
        while type(rooms_) == str:
            rooms_ = json.loads(rooms_)
            
        for judge in judges_:
            if judge["assigned"] == False:
                available_judges_list.append(judge["judgeId"])
        
        for room in rooms_:
            if room["available"] == True:
                available_rooms_list.append(room["roomId"])
        
        return available_judges_list, available_rooms_list, judges_, rooms_        
        
    def complete_round(self, lambda_client, roundStateId):
        # completeRound
        payload_room = {
            "path": "/complete_round",
            "body": {
                "roundStateId": roundStateId
            }
        }
        response = lambda_client.invoke(
            FunctionName=completeRoundHandler,
            InvocationType='Event',
            Payload=json.dumps(payload_room),
        )
        
    def get_arrange_judges(self, judges_need, total_judges, judges_list):
        if judges_need >= total_judges:
            logger.debug("********** arranged judges list **********")
            logger.debug(judges_list[:total_judges])
            return [judges_list[:total_judges]]
        
        arrang_judges_list = []
        left_bound = 0
        right_bound = judges_need
        
        while right_bound <= total_judges:
            arrang_judges_list.append(judges_list[left_bound:right_bound])
            left_bound += judges_need
            right_bound += judges_need
            
        logger.debug("********** arranged judges list **********")
        logger.debug(arrang_judges_list)
        return arrang_judges_list
    
    def get_judges_need(self, rounds, currentRoundIdx) -> int:
        judges_need = 0
        rounds = json.loads(rounds[0])
        round = rounds[currentRoundIdx]
        judges_need = round["judgesPerRound"]
        return int(judges_need)
    
    def group_assign_group_judge(self, appsyncy_query, deq_group, arrang_judges_list, available_rooms_list, roundStateObj, og_judges_list, og_rooms_list, tournamentStateInfo):
        # judges_index used to track the arranged judges
        # groups_index used to track the group
        judges_index = 0
        groups_index = 0
        while deq_group and (groups_index < len(available_rooms_list) or judges_index < len(arrang_judges_list)):
            
            group = deq_group.pop()
            
            if judges_index < len(arrang_judges_list):
                judgeIds = arrang_judges_list[judges_index]
                og_judges_list = self.use_judge(og_judges_list, judgeIds)
                group.set_judges(judgeIds)
                judges_index += 1
        
            if groups_index < len(available_rooms_list):
                roomIds = available_rooms_list[groups_index]
                og_rooms_list = self.use_room(og_rooms_list, roomIds)
                group.set_roomId(roomIds)
                groups_index += 1

            roundStateObj.queued_to_assigned(group.get_group_json())
                
        appsyncy_query.update_judges_rooms_TournamentState_query(tournamentStateInfo['id'], tournamentStateInfo['_version'], json.dumps(og_judges_list), json.dumps(og_rooms_list))