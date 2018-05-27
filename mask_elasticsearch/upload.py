from elasticsearch import Elasticsearch
from .settings import *
import json,os, datetime

def es_upload_static_testing_result(md5,result_bc,result_mc):
    es = Elasticsearch([{'host': IP, 'port': Port}])

    result_mc = str(result_mc).replace('[', "").replace(']', "").replace(" ", "")
    doc = dict()
    doc['md5'] = md5
    doc['detected'] = 1 if result_bc[0] else 0
    doc['result_bc'] = str(float("{0:.2f}".format(result_bc[1]))*100)
    doc['result_mc'] = str(result_mc)
    doc['collected_date'] = datetime.datetime.now()

    res = es.index(index=main_index, doc_type=type_static_testing,id = md5,body=doc)

def es_upload_dynamic_testing_result(md5,result_bc,result_mc):
    es = Elasticsearch([{'host': IP, 'port': Port}])

    result_mc = str(result_mc).replace('[', "").replace(']', "").replace(" ", "")
    doc = dict()
    doc['md5'] = md5
    doc['detected'] = 1 if result_bc[0] else 0
    doc['result_bc'] = str(float("{0:.2f}".format(result_bc[1]))*100)
    doc['result_mc'] = str(result_mc)
    doc['collected_date'] = datetime.datetime.now()

    res = es.index(index=main_index, doc_type=type_dynamic_testing,id = md5,body=doc)

def es_upload_peviewer_result(md5,peviewer_result):
    es = Elasticsearch([{'host': IP, 'port': Port}])

    res = es.index(index=main_index, doc_type=type_peviewer_result, id = md5, body= peviewer_result)