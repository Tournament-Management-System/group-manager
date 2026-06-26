import unittest
from unittest.mock import Mock, patch
import json
from src.Lambda.LambdaHelper import LambdaHelper

class TestGroupUtils(unittest.TestCase):

    def setUp(self):
        self.obj = LambdaHelper()

    def test_judges_need_greater_than_total_judges(self):
        judges_need = 5
        total_judges = 3
        judges_list = ['Judge A', 'Judge B', 'Judge C']
        expected_result = ['Judge A', 'Judge B', 'Judge C']
        result = self.obj.get_arrange_judges(judges_need, total_judges, judges_list)
        self.assertEqual(result, expected_result)

    def test_judges_need_equal_to_total_judges(self):
        judges_need = 3
        total_judges = 3
        judges_list = ['Judge A', 'Judge B', 'Judge C']
        expected_result = ['Judge A', 'Judge B', 'Judge C']
        result = self.obj.get_arrange_judges(judges_need, total_judges, judges_list)
        self.assertEqual(result, expected_result)

    def test_judges_need_less_than_total_judges(self):
        judges_need = 2
        total_judges = 5
        judges_list = ['Judge A', 'Judge B', 'Judge C', 'Judge D', 'Judge E']
        expected_result = [['Judge A', 'Judge B'], ['Judge C', 'Judge D']]
        result = self.obj.get_arrange_judges(judges_need, total_judges, judges_list)
        self.assertEqual(result, expected_result)
        
    def test_remaining_judges(self):
        judges_need = 2
        total_judges = 4
        judges_list = ['Judge A', 'Judge B', 'Judge C', 'Judge D']
        expected_result = [['Judge A', 'Judge B'], ['Judge C', 'Judge D']]
        result = self.obj.get_arrange_judges(judges_need, total_judges, judges_list)
        self.assertEqual(result, expected_result)
        
    def test_use_judge(self):
        og_judges_list = [{'judgeId': 1, 'assigned': False}, {'judgeId': 2, 'assigned': False}, {'judgeId': 3, 'assigned': False}]
        use_judges_id = [2, 3]
        expected_output = [{'judgeId': 1, 'assigned': False}, {'judgeId': 2, 'assigned': True}, {'judgeId': 3, 'assigned': True}]
        self.assertEqual(self.obj.use_judge(og_judges_list, use_judges_id), expected_output)

    def test_use_room(self):
        og_rooms_list = [{'roomId': 1, 'available': True}, {'roomId': 2, 'available': True}, {'roomId': 3, 'available': True}]
        use_room_id = 2
        expected_output = [{'roomId': 1, 'available': True}, {'roomId': 2, 'available': False}, {'roomId': 3, 'available': True}]
        self.assertEqual(self.obj.use_room(og_rooms_list, use_room_id), expected_output)

    def test_release_judge(self):
        judge_infos = [{'judgeId': 1, 'assigned': True}, {'judgeId': 2, 'assigned': True}, {'judgeId': 3, 'assigned': True}]
        judgeIds = [2, 3]
        expected_output = '[{"judgeId": 1, "assigned": true}, {"judgeId": 2, "assigned": false}, {"judgeId": 3, "assigned": false}]'
        self.assertEqual(self.obj.release_judge(judge_infos, judgeIds), expected_output)

    def test_release_room(self):
        room_infos = [{'roomId': 1, 'available': False}, {'roomId': 2, 'available': False}, {'roomId': 3, 'available': False}]
        roomIds = [2, 3]
        expected_output = '[{"roomId": 1, "available": false}, {"roomId": 2, "available": true}, {"roomId": 3, "available": true}]'
        self.assertEqual(self.obj.release_room(room_infos, roomIds), expected_output)

    def test_release_all_judges(self):
        judge_infos = [{'judgeId': 1, 'assigned': True}, {'judgeId': 2, 'assigned': True}, {'judgeId': 3, 'assigned': True}]
        expected_output = '[{"judgeId": 1, "assigned": false}, {"judgeId": 2, "assigned": false}, {"judgeId": 3, "assigned": false}]'
        self.assertEqual(self.obj.release_all_judges(judge_infos), expected_output)

    def test_release_all_rooms(self):
        room_infos = [{'roomId': 1, 'available': False}, {'roomId': 2, 'available': False}, {'roomId': 3, 'available': False}]
        expected_output = '[{"roomId": 1, "available": true}, {"roomId": 2, "available": true}, {"roomId": 3, "available": true}]'
        self.assertEqual(self.obj.release_all_rooms(room_infos), expected_output)

    def test_get_availableJudgesRooms(self):
        tournamentStateInfo = {'judges': json.dumps([{'judgeId': 1, 'assigned': False}, {'judgeId': 2, 'assigned': True}]), 
                            'rooms': json.dumps([{'roomId': 1, 'available': True}, {'roomId': 2, 'available': False}])}
        result = self.obj.get_availableJudgesRooms(tournamentStateInfo)
        self.assertEqual(result[0], [1])
        self.assertEqual(result[1], [1])
        self.assertEqual(result[2], [{'judgeId': 1, 'assigned': False}, {'judgeId': 2, 'assigned': True}])
        self.assertEqual(result[3], [{'roomId': 1, 'available': True}, {'roomId': 2, 'available': False}])

