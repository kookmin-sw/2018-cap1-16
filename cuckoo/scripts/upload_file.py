#-*-coding:utf-8-*-
'''
    Author : Chaeyeon Han
    Date created : 04/18/2018
    Python version : 3.6

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
    with open(file_path, 'rb') as f :
        file_name = get_file_name(file_path)
        fs = {'file' : (file_name, f)}
        r = requests.post(REST_URL,files=fs)
        print(r)
        if r.status_code == 200 :
            print("Dynamic Analysis upload : {} is succeeded".format(file_name))
            #global task_id
            task_id = r.json()["task_ids"][0]
            json_reply = status_check(task_id)
            print(json_reply)
            return json_reply
        else :
            print("{} is failed".format(file_name))
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
    api_url = os.path.join(REPORT_URL, str(taskid))
    print(api_url)
    previous_time = time.time()
    while True:
        if  time.time() - previous_time  > 1:
            response = api_request(api_url)
            print(response.status_code)
            print(response.text)
            if response.status_code == 200 :
                break
            previous_time = time.time()
    json_reply = json.loads(response.text)
    return json_reply

def api_request(url):
    response = requests.get(url)
    return response


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

