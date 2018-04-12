#-*-coding:utf-8-*-
import json
import sys, os
import pickle

REPORT = "/home/seclab/toyexample_report"
PICKLE = "/home/seclab/toyexample_pickle"

def apiExtract(file_path = REPORT):
    reports = os.listdir(file_path)
    for r in reports :
        api_list = []
        report = os.path.join(file_path, r)
        with open(report) as f:
            json_data = json.load(f)
            try:
                processes = json_data["behavior"]["processes"]
                md5 = json_data["target"]["file"]["md5"]
            except:
                continue
            for i in range(0, len(processes)):
                if processes[i]["track"] == True:
                    for j in range(0, len(processes[i]["calls"])):
                        api_list.append(processes[i]["calls"][j]["api"])
        pickle_dir = os.path.join(PICKLE, md5+".acs")
        with open(pickle_dir, 'wb') as p:
            pickle.dump(api_list, p)

if __name__ == '__main__':
    apiExtract() 
