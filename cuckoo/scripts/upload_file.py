#-*-coding:utf-8-*-
'''
    Author : Chaeyeon Han
    Date created : 04/18/2018
    Date modified : 04/22/2018
    Python version : 3.6

    pip install request
    execution : "python3 upload_file.py [file directory] ([cpu count])"

'''

import requests, os
import threading
import time, sys
import multiprocessing as mp
import json

REST_URL = "http://203.246.112.138:8090/tasks/create/submit"
REPORT_URL = "http://203.246.112.138:8090/tasks/report"

status = ''

def get_file_name ( file_path ) :
    return os.path.basename(file_path)

def send_file( file_path ) :
    print(file_path)
    with open(file_path, 'rb') as f :
        file_name = get_file_name(file_path)
        fs = {'file' : (file_name, f)}
        res = requests.post(REST_URL,files=fs)
        if res.status_code == 200 :
            print("upload : {} is succeeded".format(file_name))
            task_id = res.json()["task_ids"][0]
            response_data = status_check(task_id)
            return response_data
        else :
            print("upload : {} is failed".format(file_name))
            return None

def run( root , process_count = os.cpu_count() ) :
    file_path = root
    mp.freeze_support()
    response_data = send_file(file_path)
    return response_data

def status_check(taskid = None):
    if taskid is None or taskid < 1:
        print("Task id is wrong")
        return
    global request
    api_url = REPORT_URL+ "/" + str(taskid)
    previous_time = time.time()
    while True:
        if  time.time() - previous_time  > 1:
            res = api_request(api_url)
            print(res.text)
            if res.status_code == 200 :
                break
            previous_time = time.time()
    json_reply = json.loads(res.text)
    print(json_reply)
    return json_reply

def api_request(url):
    resp = requests.get(url)
    return resp


if __name__ == '__main__' :
    if len(sys.argv) == 2 :
        start = time.time()
        run(sys.argv[1])
        print("Time : {}".format(time.time() - start))
        #print(task_id)
    elif len(sys.argv) == 3 :
        start = time.time()
        run(sys.argv[1], int(sys.argv[2]))
        print("Time : {}".format(time.time() - start))

