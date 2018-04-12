#-*-coding:utf-8-*-
import requests, os

import time, sys
import multiprocessing as mp

REST_URL = "http://192.168.56.1:8090/tasks/create/file"

def explorer( root ):
    ret = []
    for path, dir, files in os.walk(root) :
        for file in files :
            ret.append(os.path.join(path, file))
    return ret

def get_file_name ( file_path ) :
    return os.path.basename(file_path)

def send_file( file_path ) :
    with open(file_path, 'rb') as f :
        file_name = get_file_name(file_path)
        fs = {'file' : (file_name, f)}
        r = requests.post(REST_URL, files=fs)
        if r.status_code == 200 :
            print("{} is succeeded".format(file_name))
        else :
            print("{} is failed".format(file_name))

def run( root , process_count = os.cpu_count() ) :
    file_path_list = explorer(root)
    mp.freeze_support()
    p = mp.Pool( process_count )
    p.map(send_file, file_path_list)

if __name__ == '__main__' :
    if len(sys.argv) == 2 :
        start = time.time()
        run(sys.argv[1])
        print("Time : {}".format(time.time() - start))
    elif len(sys.argv) == 3 :
        start = time.time()
        run(sys.argv[1], int(sys.argv[2]))
        print("Time : {}".format(time.time() - start))

