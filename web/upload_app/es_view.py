from elasticsearch import Elasticsearch
import sys

es = Elasticsearch([{'host':'203.246.112.133','port':9200}])

def es_md5_search(file_md5):
    #request_data = {'query':{'term':{'_id':file_md5}}}
    request_data = {'query':{'term':{'_id':'ac7dd458cd8569199c67f0253cf039ec'}}}

    res = es.search(index="seclab",  body=request_data)
    if res['hits']['total'] is not 0 :
        return res['hits']['hits'][0]
    else:
        return 0

def es_ssdeep_search(ssdeep):
    ssdeep_data = ssdeep.split(":")
    ssdeep_size = int(ssdeep_data[0])
    ssdeep_chunk = ssdeep_data[1]
    ssdeep_double_chunk = ssdeep_data[2]
    
    request_data = \
    {
        'query':{
            'bool':{
                'must':[{
                    'term':{'SSDeep_chunk_size':ssdeep_size},
                    },{
                    'bool':{
                        'should':{
                            'match':{
                                'SSDeep_chunk':{
                                    'query': ssdeep_chunk
                                }
                            }
                        }
                    }
                }]
            }
        }
    }
    res = es.search(index="seclab",  body=request_data)
    #sys.stderr.write(str(res['hits']['hits']))     
    if res['hits']['total'] is not 0 :
        return res['hits']['hits']
    else:
        return 0                 
