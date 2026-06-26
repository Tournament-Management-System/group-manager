import json
from constants.DecimalEncoder import DecimalEncoder
def eventMetaData():
    return {
        "eventId": "testeventId",
        "awards": [
            {
            "awardName": "Finalists",
            "numWinners": "6",
            "awardCriteria": "highest_last_round"
            },
            {
            "awardName": "Sweepstake",
            "numWinners": "6",
            "awardCriteria": "highest_all_rounds"
            }
        ],
        "currentRoundIdx" : 2,
        "rounds": [
            {
            "roundId": "0",
            "competitorLimit": 6,
            "groupLimit": None,
            "judgesPerRound": 1,
            "judgingCriteria": None
            },
            {
            "roundId": "1",
            "competitorLimit": 6,
            "groupLimit": None,
            "judgesPerRound": 1,
            "judgingCriteria": None
            },
            {
            "roundId": "2",
            "competitorLimit": 6,
            "groupLimit": 3,
            "judgesPerRound": 3,
            "judgingCriteria": None
            },
            {
            "roundId": "3",
            "competitorLimit": 6,
            "groupLimit": 1,
            "judgesPerRound": 3,
            "judgingCriteria": None
            }
        ]}
    
def roundData_startGroups():
    return {
        "roundId": "2",
        "assigned": [],
        "queued": [
            { "competitors": ["c1", "c2"], "groupId": "0", "judges": [], "ranking": { } },
            { "competitors": ["c3", "c4"], "groupId": "1", "judges": [], "ranking": { } },
            { "competitors": ["c5", "c6"], "groupId": "2", "judges": [], "ranking": { } },
            { "competitors": ["c14", "c12"], "groupId": "3", "judges": [], "ranking": { } },
            { "competitors": ["c9", "c8"], "groupId": "4", "judges": [], "ranking": { } },
            { "competitors": ["c14", "c9"], "groupId": "5", "judges": [], "ranking": { } }
            ],
        "completed": [],
        "started": []
    }
    
def groupData():
    return [
            { "competitors": ["c1", "c2"], "groupId": "0", "judges": [], "ranking": { } },
            { "competitors": ["c3", "c4"], "groupId": "1", "judges": [], "ranking": { } },
            { "competitors": ["c5", "c6"], "groupId": "2", "judges": [], "ranking": { } },
            { "competitors": ["c14", "c12"], "groupId": "3", "judges": [], "ranking": { } },
            { "competitors": ["c9", "c8"], "groupId": "4", "judges": [], "ranking": { } },
            { "competitors": ["c14", "c9"], "groupId": "5", "judges": [], "ranking": { } }
            ]

def roundData_startCompetition():
    return {
            'roundId' : "2",
            'QUEUED' : [],
            'ASSIGNED': [
                {'groupId': 'group001',
                'roomId' : 'abcroomd',
                'judgesIds': ['aaa', 'bbb'],
                'competitorIds': ['c1', 'c2','c3'],
                'judgeingresult': {
                    
                }}
                ],
            'STARTED' : [],
            'COMPLETED': []
            }

def roundData_collectResult():
    return {
            'roundId' : '000001',
            'QUEUED' : [],
            'ASSIGNED': [],
            'STARTED' : [
                {'groupId': 'group001',
                'roomId' : 'abcroomd',
                'judgesIds': ['aaa', 'bbb'],
                'competitorIds': ['c1', 'c2','c3'],
                'judgeingresult': {}
                }
                ],
            'COMPLETED': []
            }