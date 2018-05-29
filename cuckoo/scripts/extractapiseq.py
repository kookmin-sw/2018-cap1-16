#-*-coding:utf-8-*-
import json
import sys, os
import pickle

DIRECTORY = "/home/seclab/.cuckoo/storage/analyses/"

def api_extract(dir, file_cnt,DIRECTORY):
    total_cnt = 0
    task_list = os.listdir(DIRECTORY)
    for task in range(1, int(file_cnt)+1):
        api_list  = []
        task_dir_name = DIRECTORY + str(task) + "/reports/"
        task_path = task_dir_name + "report.json"
        with open(task_path) as f:
            json_data = json.load(f)
            md5 = json_data["target"]["file"]["md5"]
            try:
                processes = json_data["behavior"]["processes"]
                for i in range(0, len(processes)):
                    if processes[i]["track"] == True:
                        for j in range(0, len(processes[i]["calls"])):
                            api_list.append(processes[i]["calls"][j]["api"])
            except:
                pass
            if (len(api_list) >= 5):
                pickle_dir = os.path.join(dir, md5 + ".acs")
                with open(pickle_dir, 'wb') as p:
                    pickle.dump(api_list, p)
                total_cnt += 1

            
if __name__ == '__main__':
    pickle_dir = sys.argv[1]
    cnt = sys.argv[2]
    cuckoo_dir = sys.argv[3]
    api_extract(pickle_dir,cnt,cuckoo_dir)
