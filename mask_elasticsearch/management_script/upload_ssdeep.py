from datetime import datetime
from elasticsearch import Elasticsearch
from ..settings import *
import json,os

es = Elasticsearch([{'host':IP,'port':Port}])

DIRECTORY_PATH = '/home/seclab/ssdeep_report/'

def index_report(path):
    files = os.listdir(path)
    file_count = len(files)
    remain_count = file_count
    for file in files:
        absolute_path = os.path.join(path,file)
        report_json = open(absolute_path).read()
        doc = json.loads(report_json)
        res = es.index(index=ssdeep_index, doc_type=type_ssdeep,id = md5,body=doc)
        print('Index suecceeded ('+str(remain_count)+'/'+str(file_count)+')')
        remain_count -=1

if __name__ == '__main__':
    index_report(DIRECTORY_PATH)