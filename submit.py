import requests
import json
import argparse
import urllib3
"""

成功：
{
    "status":1,
    "msg":"success",
    "questionScore":128,   //得分
    "questionRank":1    //本次提交题目排名
}

失败：
{
    "status":0,
    "msg":"提示信息"
}
"""

def submit(host, port , username, password, answer):

    data = { 'answer': answer,}
    try:
        r = requests.post('https://{}:{}/api/sub_answer'.format(host, port), data=data, verify=False, auth=(username, password), timeout=3)
        # r = requests.post('http://{}:{}/api/sub_answer'.format(host, port), data=data, verify=False, auth=(username, password), timeout=3)
        if r.status_code != 200:
            raise ValueError('get qeustion status error: {0}'.format(r.status_code))
    except Exception as e:
        print(e)
        return False

    result = json.loads(r.text)
    if result['status'] == 1:
        return (True, result['msg'])
    else:
        print('[-] ' + result['msg'])
        return (False, result['msg'])

def main(args):
    if submit(args.host, args.port, args.user, args.password, args.flag)[0]:
        print('[+] sucessfully submitted')
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RHG flag submit script')
    parser.add_argument('--host', type=str, help='RHG server address')
    parser.add_argument('--port', type=str, help='RHG server port', default=80)
    parser.add_argument('--user', type=str, help='RHG user name')
    parser.add_argument('--pass', type=str, help='RHG user password', dest='password')
    parser.add_argument('--flag', type=str, help='challenge flag')
    urllib3.disable_warnings()
    args = parser.parse_args()
    if args.host == None or args.user == None or args.password == None:
        parser.print_help()
        exit(1)
    
    main(args)
