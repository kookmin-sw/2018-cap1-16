from elasticsearch import Elasticsearch
from .settings import *
import sys

es = Elasticsearch([{'host':IP,'port':Port}])

def es_static_report_search(md5):

    request_data = \
        {
            'query': {
                "term": {
                    "md5": md5
                }
            }
        }
    res = es.search(index=main_index, body=request_data)
    if res['hits']['total'] is not 0:
        return res['hits']['hits'][0]['_source']
    else:
        return None

def es_static_testing_result_search(md5):
    request_data = \
        {
            'query': {
                "term": {
                    "md5": md5
                }
            }
        }
    res = es.search(index=main_index,doc_type=type_static_testing, body=request_data)
    if res['hits']['total'] is not 0:
        return res['hits']['hits'][0]['_source']
    else:
        return None

def es_dynamic_report_search(md5):

    request_data = \
        {
            '_source': ["target.file","signatures","summary.dll_loaded","summary.connects_host","summary.connects_ip","report_time"],
            'query': {
                "term": {
                    "target.file.md5": md5
                }
            }
        }
    res = es.search(index=cuckoo_index, body=request_data)
    #print (res['hits']['hits'][0]['_source'])
    if res['hits']['total'] is not 0:
        return res['hits']['hits'][0]['_source']
    else:
        return None

def es_dynamic_testing_result_search(md5):
    request_data = \
        {
            'query': {
                "term": {
                    "md5": md5
                }
            }
        }
    res = es.search(index=main_index,doc_type=type_dynamic_testing, body=request_data)
    if res['hits']['total'] is not 0:
        return res['hits']['hits'][0]['_source']
    else:
        return None

def es_search_peviewer_result(md5):
    request_data = \
        {
            'query': {
                "term": {
                    "_id": md5
                }
            }
        }
    res = es.search(index=main_index,doc_type=type_peviewer_result, body=request_data)
    if res['hits']['total'] is not 0:
        return res['hits']['hits'][0]['_source']
    else:
        return None

def es_search_similar_file(ssdeep):
    ssdeep = ssdeep.split(":")
    ssdeep_size = int(ssdeep[0])
    ssdeep_chunk = ssdeep[1]
    ssdeep_double_chunk = ssdeep[2]
    request_data = \
        {
            'query': {
                'bool': {
                    'must': [{
                        'term': {'chunk_size': ssdeep_size},
                    }, {
                        'bool': {
                            'should': {
                                'match': {
                                    'chunk': {
                                        'query': ssdeep_chunk
                                    }
                                }
                            }
                        }
                    }]
                }
            }
        }
    res = es.search(index=ssdeep_index,doc_type=type_ssdeep, body=request_data)
    if res['hits']['total'] is not 0:
        return res['hits']['hits']
    else:
        return None