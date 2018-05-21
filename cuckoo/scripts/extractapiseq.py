#-*-coding:utf-8-*-
import json
import sys, os
import pickle

REPORT = "/home/seclab/170728_report"
PICKLE = "/home/seclab/170728_acs"


def apiExtract(file_path = REPORT):
    total_cnt = 0
    reports = os.listdir(file_path)
    
    md5_txt_file = open(os.path.join(PICKLE,'md5_170728.txt'),'w')
    for r in reports :
        api_list = []
        report = os.path.join(file_path, r)
        with open(report) as f:
            json_data = json.load(f)
            md5 = json_data["target"]["file"]["md5"]
            try:
                processes = json_data["behavior"]["processes"]
            except:
                pass
            try:
                for i in range(0, len(processes)):
                    if processes[i]["track"] == True:
                        for j in range(0, len(processes[i]["calls"])):
                            api_list.append(processes[i]["calls"][j]["api"])
            except:
                pass
            if(len(api_list)>=5):
                pickle_dir = os.path.join(PICKLE, md5+".acs")
                with open(pickle_dir, 'wb') as p:
                    pickle.dump(api_list, p)
                md5_txt_file.write(md5+'\n')
                total_cnt += 1
                
    md5_txt_file.close()
            
if __name__ == '__main__':
    apiExtract() 
