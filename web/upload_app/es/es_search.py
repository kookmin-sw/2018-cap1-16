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

def es_dynamic_report_search(md5):

    request_data = \
        {
            '_source': ["target.file","signatures","summary.dll_loaded"],
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

def es_ssdeep_search(ssdeep):

    ssdeep_data = ssdeep.split(":")
    ssdeep_size = int(ssdeep_data[0])
    ssdeep_chunk = ssdeep_data[1]
    ssdeep_double_chunk = ssdeep_data[2]

    request_data = \
        {
            'query': {
                'bool': {
                    'must': [{
                        'term': {'SSDeep_chunk_size': ssdeep_size},
                    }, {
                        'bool': {
                            'should': {
                                'match': {
                                    'SSDeep_chunk': {
                                        'query': ssdeep_chunk
                                    }
                                }
                            }
                        }
                    }]
                }
            }
        }
    res = es.search(index=main_index, body=request_data)
    # sys.stderr.write(str(res['hits']['hits']))
    if res['hits']['total'] is not 0:
        return res['hits']['hits']
    else:
        return None
