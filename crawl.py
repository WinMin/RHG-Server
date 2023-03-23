import requests
import json
import argparse
import pprint
import urllib3


def getChallInfo(host, port, user, password):

    """
    example: curl -k -X GET --user user:pwd https://172.20.1.11/api/get_question_status
    return is json:  
    """
    try:
        r = requests.get('https://{}:{}/api/get_question_status'.format(host, port), verify=False, auth=(user, password), timeout=3)
        if r.status_code != 200:
            raise ValueError('get qeustion status error: {0}'.format(r.status_code))
    except Exception as e:
        print(e)
        return False
    result = json.loads(r.text)
    # print(result)
    return result

def resetChallStatus(host, port, user, password, challid):
    """
    curl -k -d "ChallengeID=1" -X POST -v --user user:pwd https://172.20.1.11/api/reset_question
    return is json
    频率限制：60秒（60秒内只能重置一次）
    成功：{"status":1,"msg":"success"}
    失败：{"status":0,"msg":"提示信息"}
    """
    data = {
    'ChallengeID': challid,
    }
    try:
        r = requests.post('https://{}:{}/api/reset_question'.format(host, port), data=data, verify=False, auth=(user, password), timeout=3)
        if r.status_code != 200:
            raise ValueError('reset qeustion failed: {}'.format(r.status_code))
    except Exception as e:
        print(e)
        return False
    result = json.loads(r.text)
    return result

def getRanking(host, port, user, password):
    """
    https://172.20.1.11/api/get_ranking
    curl -k -X GET --user user:pwd https://172.20.1.11/api/get_ranking
    return json


    [
        {
            "rank": 1,//排名
            "team_name": "team1",//战队名称
            "total_score": 128,//队伍总分
            "first_blood_num": 1,//一血数量
            "answer_count": 2,//答题数量
        },

                {
            "rank": 2,//排名
            "team_name": "team2",//战队名称
            "total_score": 128,//队伍总分
            "first_blood_num": 1,//一血数量
            "answer_count": 2,//答题数量
        },
    ]
    """

    try:
        r = requests.get('https://{}:{}/api/get_ranking'.format(host, port), verify=False, auth=(user, password), timeout=3)
        if r.status_code != 200:
            raise ValueError('get ranking failed: {}'.format(r.status_code))
        result = json.loads(r.text)
        return result
    except Exception as e:
        print(e)
        return False
    
def getMachinesInfo(host, port, user, password, **kwargs):
    """
    https://172.20.1.11/api/get_machines_info
    curl -k -X GET --user user:pwd https://172.20.1.11/api/get_machines_info
    return json
    """

    try:
        r = requests.get('https://{}:{}/api/get_machines_info'.format(host, port), verify=False, auth=(user, password), timeout=3)
        if r.status_code != 200:
            raise ValueError('get machines info failed: {}'.format(r.status_code))
        result = json.loads(r.text)
        return result
    except Exception as e:
        print(e)
        return False


def main(args):
    json_data = getChallInfo(args.host, args.port, args.user, args.password)
    if not json_data:
        exit()
    pprint.pprint(json_data)
    

if __name__ == '__main__':

    urllib3.disable_warnings()

    parser = argparse.ArgumentParser('A junk tool for RHG')
    parser.add_argument('--host', type=str, help='RHG server address')
    parser.add_argument('--port', type=str, help='RHG server port', default=443)
    parser.add_argument('--user', type=str, help='RHG user name')
    parser.add_argument('--pass', type=str, help='RHG user password', dest='password')
    
    subparsers = parser.add_subparsers()

    parser_getChallInfo = subparsers.add_parser('getchallinfo', help='get challenge info')
    parser_getChallInfo.set_defaults(func=getChallInfo)

    parser_resetChallStatus = subparsers.add_parser('resetchallstatus', help='reset challenge status')
    parser_resetChallStatus.add_argument('--challid', type=str, help='challenge id')
    parser_resetChallStatus.set_defaults(func=resetChallStatus)

    parser_getRanking = subparsers.add_parser('getranking', help='get ranking')
    parser_getRanking.set_defaults(func=getRanking)

    parser_getMachinesInfo = subparsers.add_parser('getmachinesinfo', help='get machines info')
    parser_getMachinesInfo.set_defaults(func=getMachinesInfo)


    args = parser.parse_args()

    if args.host == None or args.user == None or args.password == None:
        parser.print_help()
        exit(1)

    if hasattr(args, 'func'):
        args_dict = vars(args)
        func = args_dict.pop('func')
        pprint.pprint(func(**args_dict))