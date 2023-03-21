from flask import Flask, jsonify, request, Response

app = Flask(__name__)

@app.route('/api/get_question_status', methods=['GET'])
def get_question_status():
    AiChallenge = [{
        "challengeID": 1,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 10,
        "current_score": 128,
        "score": 0,
        "question_type": 1,
    },
    {
        "challengeID": 3,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 0,
        "question_type": 2,
    },

        {
        "challengeID": 2,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 0,
        "question_type": 2,
    },

    {
        "challengeID": 4,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 128,
        "question_type": 2,
    },

        {
        "challengeID": 5,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 128,
        "question_type": 2,
    },

        {
        "challengeID": 6,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 128,
        "question_type": 2,
    },

    {
        "challengeID": 7,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "http://172.16.48.192:8001/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 128,
        "question_type": 2,
    },

    {
        "challengeID": 8,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 128,
        "question_type": 2,
    },
    {
        "challengeID": 9,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 128,
        "question_type": 2,
    },
    {
        "challengeID": 10,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https://172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 128,
        "question_type": 2,
    },
        {
        "challengeID": 11,
        "vm_ip": "127.0.0.1",
        "question_port": 8080,
        "binaryUrl": "https:#172.20.1.11/resources/fileupload/xxx/bin",
        "flag_path": "/home/flag1.txt",
        "first_blood": 0,
        "current_time": 1547717696,
        "attacks_count": 0,
        "current_score": 128,
        "score": 128,
        "question_type": 2,
    },


    
    ]

    PointsInfo = [{
        "aiPoints": 60,
    }]

    response = {
        "status": 1,
        "AiChallenge": AiChallenge,
        "PointsInfo": PointsInfo
    }

    return jsonify(response)

@app.route("/api/sub_answer", methods=['POST'])
def post_answer():
    answer = request.form.get('answer')
    if answer == 'flag{this_is_a_flag}':
        response = {
            "status": 1,
            "msg":"success",
            "questionScore":128, 
            "questionRank":1    
        }
    else:
        response = {
            "status":0,
            "msg":"flag 错误"
        }


    return jsonify(response)

@app.route("/api/reset_question", methods=['POST'])
def post_reset():
    user = request.authorization.get('username')
    pwd = request.authorization.get('password')
    print(user, pwd)
    ChallengeID = request.form.get('ChallengeID')
    print('ChallangeID: {}'.format(ChallengeID))
    respose = {
        "status" : 1,
        "msg" : "success"
    }
    return jsonify(respose)


@app.route("/api/get_ranking", methods=['GET'])
def get_rank():
    user = request.authorization.get('username')
    pwd = request.authorization.get('password')
    print(user, pwd)

    response =  [
        {
            "rank": 1,
            "team_name": "team1",
            "total_score": 500,
            "first_blood_num": 1,
            "answer_count": 2,
        },

        {
            "rank": 2,
            "team_name": "team2",
            "total_score": 399,
            "first_blood_num": 1,
            "answer_count": 2,
        },

        {
            "rank": 3,
            "team_name": "team3",
            "total_score": 228,
            "first_blood_num": 1,
            "answer_count": 2,
        },


        {
            "rank": 4,
            "team_name": "team4",
            "total_score": 128,
            "first_blood_num": 1,
            "answer_count": 2,
        },


        {
            "rank": 5,
            "team_name": "team5",
            "total_score": 28,
            "first_blood_num": 1,
            "answer_count": 2,
        },

    ]
        
    return jsonify(response)

@app.route("/api/get_machines_info", methods=['GET'])
def get_machines_info():
    user = request.authorization.get('username')
    pwd = request.authorization.get('password')
    print(user, pwd)   

    response = [
    {
        "name":"test1",
        "questions":[
            {
                "challengeID":18,
                "is_running":"true",
                "connection_number":2# 进程连接数
            }
        ],
        "virtual_memory":{# 服务器内存信息
            "available":428322816,# 已获取内存
            "used":450215936,# 已使用内存
            "cached":194371584, # 缓存
            "percent":58.5, # 百分比
            "free":387031040,# 剩余内存
            "shared":9244672,# 共享内存
            "total":1032589312# 总物理内存
        },
        "cpu":{# CPU信息
            "physical_count":1,# 物理数量
            "logical_count":1,# 逻辑数量
            "percent":21.9 # 资源百分比 0.1/s
        },
        "swap_memory":{# 交换内存信息
            "used":0,# 已使用
            "total":2147479552,# 总量
            "percent":0,# 百分比
            "free":2147479552 # 剩余
        },
        "process_number":130# 服务器进程数
    },
       {
        "name":"test2",
        "questions":[
            {
                "challengeID":3,
                "is_running":"true",
                "connection_number":2# 进程连接数
            }
        ],
        "virtual_memory":{# 服务器内存信息
            "available":428322816,# 已获取内存
            "used":450215936,# 已使用内存
            "cached":194371584, # 缓存
            "percent":58.5, # 百分比
            "free":387031040,# 剩余内存
            "shared":9244672,# 共享内存
            "total":1032589312# 总物理内存
        },
        "cpu":{# CPU信息
            "physical_count":1,# 物理数量
            "logical_count":1,# 逻辑数量
            "percent":21.9 # 资源百分比 0.1/s
        },
        "swap_memory":{# 交换内存信息
            "used":0,# 已使用
            "total":2147479552,# 总量
            "percent":0,# 百分比
            "free":2147479552 # 剩余
        },
        "process_number":130# 服务器进程数
    },

]
        

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, ssl_context='adhoc')