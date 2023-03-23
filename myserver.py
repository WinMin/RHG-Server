from pywebio.platform.flask import webio_view
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import register_thread
import pyecharts.options as opts
from pyecharts.charts import Line
from flask import Flask
import argparse
from threading import Thread, Lock
import requests
import os
import urllib3
import datetime
import time
import json

import crawl
import submit

app = Flask(__name__)
urllib3.disable_warnings()

def put_mainbav():
    put_html("""
        <body style="background-color: black;">

            <style>
                #navbar a {
                    display: inline-block;
                    color: white;
                    text-align: center;
                    padding: 14px 16px;
                    text-decoration: none;
                }
                #navbar a:hover {
                    background-color: black;
                    color: white;
                }
                #navbar {
                    background-color: black;
                    overflow: hidden;
                }
            </style>
      
            <div id="navbar">
                <div class="row">
                    <div class="col-12">
                        <div class="d-flex justify-content-between">
                            <div>
                                <a href="/?app=challenges" class="navbar-brand">
                                RHG Server
                                </a>
                                <a class="nav-link" href="/?app=challenges">Challenges</a>
                                <a class="nav-link" href="/?app=scoreboard">Scoreboard</a>
                                <a class="nav-link" href="/?app=about">About</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
    """ 

    )

@app.route("/")
def index():
    challenges()

def get_chall_details():

    quest_details = crawl.getChallInfo(host=HOST, port=PORT, user=USERNAME, password=PASSWORD)
    if quest_details :
        quest_details = quest_details['AiChallenge']
        return quest_details
    else:
        return False

def show_reset_result(challengeID):
    result = crawl.resetChallStatus(host=HOST, port=PORT, user=USERNAME, password=PASSWORD, challid=challengeID)
    with use_scope('challenge_details', clear=True):
        popup(
            'Challenge {} Reset Result'.format(challengeID), 
            [   
                put_text('\n\n{}'.format(result)),
            ]
        )

def show_get_machine_info(challInfo):
    data = None
    result = crawl.getMachinesInfo(host=HOST, port=PORT, user=USERNAME, password=PASSWORD)
    if result:
        for x in result: 
            if x['questions'][0]['challengeID'] == challInfo['challengeID']:
                data = x
        
        if data != None:
            machine_name = data['name']
            cpu_percent = data['cpu']['percent']
            mem_percent = data['virtual_memory']['percent']
            process_number = data['process_number']
            connection_number = data['questions'][0]['connection_number']
            MacheInfo = [
                put_markdown('#### Name: {}'.format(machine_name)),
                put_text('CPU: {}%'.format(cpu_percent)),
                put_text("Memory: {}%".format(mem_percent)),
                put_text('Porcess: {}'.format(process_number)),
                put_text('Conn Number: {}'.format(connection_number))
            ]
        else:
            MacheInfo = [
                put_text('No machine information found with challenge ID {}.'.format(challInfo['challengeID']))
            ]
        with use_scope('challenge_details', clear=True):
            popup(
                'Machine Info', MacheInfo
            )

def show_challenge_details(chalDetails):
    # print('[+] challID: {}'.format(chalDetails['challengeID']))
    chal = chalDetails
    with use_scope('challenge_details', clear=True):
        popup('题目ID: {}'.format(chal['challengeID']), [
            put_table([
                ['Type', 'Content'],
                ['server:', 'nc {} {}'.format(chal['vm_ip'], chal['question_port'])],
                ['flag  ',  chal['flag_path']],
                ['solve ',  chal['attacks_count']],   
                ['attachments:',  put_link('Link', chal['binaryUrl'])]
            ]),
                put_row(
                    [
                        put_button('Reset Chall', onclick= lambda:show_reset_result(chal['challengeID']), color='dark'),
                        put_button('Get Machine Info', onclick= lambda:show_get_machine_info(chal), color='dark')
                    ]
                )
            
            ])

def show_all_challenge(quest_details, type):
    """
    Display all the challenges in the form of multiple buttons.
    """
    buttons_list = []
    buttons_func_list = []
    for chal in quest_details:
        if chal['question_type'] == type:
            if chal['score'] != 0: 
                color='success'
            else: 
                color='primary'
            buttons_list.append(dict(label="题目ID {}".format(chal['challengeID']), value=chal, color=color))
        
        # If the download switch is turned on, then download the file.
        if DOWNLOAD:
            download_params = [chal['binaryUrl'] , chal['challengeID']]
            t = Thread(target=download, args=download_params)
            t.start()
    put_row(
        put_buttons(buttons_list, show_challenge_details)
    )

def show_submit_res(data):
    """
    show submit flag result from server
    """
    res = submit.submit(HOST, PORT, USERNAME, PASSWORD, data)
    with use_scope('submit_res', clear=True):
        put_text('Flag: {}\nMsg: {}'.format(data, res[1] ))

def show_challenges():
    """
    Challenges pages , show challenge and submit form
    """
    put_markdown('## Challenges Info : ')
    chall_details = get_chall_details()
    if chall_details :
        put_file('challenge_info.json', str(chall_details).encode('latin'))
        chall_details.sort(key = lambda x:x['challengeID']) 
        put_markdown("### Heap challenge:")
        show_all_challenge(chall_details, 2) #  challenge type , 1 is stack，2 is heap
        put_markdown("### Stack challenge:")
        show_all_challenge(chall_details, 1)

        put_markdown('---')
        put_markdown('**Submit Flag:** ')

        put_input('FLAG', help_text='Flag')
        put_buttons([dict(label='Submit', value='s', color='dark')], onclick = lambda _: show_submit_res(pin.FLAG))

def download(urlParam, IDParam):
    url = urlParam
    challID = IDParam
    try:
        if not os.path.exists('./download/{}/bin'.format(challID)):
            if not os.path.exists('./download/{}'.format(str(challID))):
                os.makedirs('./download/{}'.format(str(challID)))
            print("[+] New directory created successfully.")
            print("[+] Download url is : {}".format(url))
            r = requests.get(url, verify=False, timeout=10)
            if r.status_code != 200:
                raise ValueError('[-] get qeustion status error: {}'.format(r.status_code))
            with open('./download/{}/bin'.format(challID), 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print('[-] Download challenge binary error: {}'.format(str(e)))
        return False

@app.route("/challenges")    
def challenges():
    put_mainbav()
    try:
        show_challenges()
    except Exception as e:
        print('[-] get challenge info error: {}'.format(str(e)))

def show_scoreboard():

    put_markdown("## Scoreboard")
    MUTEX.acquire(10)
    with open("scoreboard.json", "r") as f:
        data = json.load(f)
    MUTEX.release()
    # show scoreboard line
    c = (
        Line()
        .add_xaxis(data["timeline"])
        .set_global_opts(title_opts=opts.TitleOpts(title="TOP 10 Teams"))
    )
    for team in data["teams"]:
        c.add_yaxis(team, data["teams"][team])
    c.width = "80%"
    with use_scope("socreboard_line", clear=True):
        put_html(c.render_notebook())

    # show scoreboard table
    rank_data = crawl.getRanking(HOST, PORT, USERNAME, PASSWORD)
    if rank_data:
        rank_data.sort(key=lambda x: x["rank"])
        table_data = [[d["rank"], d["team_name"], d["total_score"], d["answer_count"]] for d in rank_data]
        if len(table_data) > 20:
            table_data = table_data[:20]

        # put_table(tdata)
        put_table(tdata=table_data, header=["Rank", "Team Name", "Total Score", "Answer Count"])

@app.route("/scoreboard")
def scoreboard():
    put_mainbav()
    try:
        show_scoreboard()
    except Exception as e:
        print('[-] get scoreboard info error: {}'.format(e))

def process_score_data(rank_data, score_data_json):

    rank_data.sort(key=lambda x: x["rank"])
    if len(rank_data) > 10:
        rank_data = rank_data[:10]
    for d in rank_data:
        score_data_json["teams"][d["team_name"]].append(d["total_score"])
    now = datetime.datetime.now()
    score_data_json["timeline"].append(now.strftime("%H:%M"))
    return score_data_json

def save_scoreboard_data():
    print("[+] Start save scoreboard data ...")
    rank_data = crawl.getRanking(HOST, PORT, USERNAME, PASSWORD)
    if rank_data:
        score_data_json = {
            "teams": { d["team_name"]:[] for d in rank_data},
            "timeline": []
        }
    else:
        raise ValueError("[-] get rank data error !")

    while True:
        rank_data = crawl.getRanking(HOST, PORT, USERNAME, PASSWORD)
        if not rank_data:
            raise ValueError("[-] get rank data error !")
        score_data_json = process_score_data(rank_data, score_data_json)
        if score_data_json:
            MUTEX.acquire(10) # Lock 
            with open("scoreboard.json", "w") as f:
                f.write(json.dumps(score_data_json))
            MUTEX.release() # Unlock  

        time.sleep(ROUND)

@app.route("/about")
def about():
    put_mainbav()
    put_markdown("## About")
    put_html("<br>")
    put_code("""
    print("Fxxk ichunqiu !!!!")
    """)

def main():
    pywebio.config(title='RHG Server')
    t = Thread(target=save_scoreboard_data)
    t.start()
    pywebio.platform.flask.start_server([index, challenges, scoreboard, about], port=8080  )
    

if __name__ == '__main__':
    import pywebio
    
    parser = argparse.ArgumentParser(description = 'RHG HTTP Server')
    parser.add_argument('--host', default='172.20.1.11', type=str, help='RHG server address')
    parser.add_argument('--port', default='443', type=str, help='RHG server port')
    parser.add_argument('--user', default='admin', type=str, help='RHG user name')
    parser.add_argument('--pass', default='admin', type=str, help='RHG user password', dest='password')
    parser.add_argument('--round',default=60, type=int, help='RHG round time (s)')
    parser.add_argument('--download', action='store_true', default=False, help='automatically download attachments to the default download directory')

    args = parser.parse_args()
    HOST = args.host
    PORT = args.port
    USERNAME = args.user
    PASSWORD = args.password
    DOWNLOAD = args.download
    ROUND    = args.round
    MUTEX = Lock()

    main()  
    

