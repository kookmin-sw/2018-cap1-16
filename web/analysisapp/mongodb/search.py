from .client import MyMongoClient
import sys


def mongo_acs_search(md5):
    client = MyMongoClient('203.246.112.133', 27017, 'cuckoo')
    collection_analysis = client.db['analysis']
    collection_calls = client.db['calls']
    acs = list()

    response_md5 = collection_analysis.find_one({"target.file.md5": md5},{'behavior.processes':1})
    for process in response_md5['behavior']['processes']:
        if not len(process['calls']) == 0:
            calls_ObjectId = process['calls'][0]

            response_calls = collection_calls.find_one({"_id":calls_ObjectId},{"calls":1})
            for call in response_calls['calls']:
                acs.append(call['api'])


    return acs

def mongo_testing_result_search(md5):
    client = MyMongoClient('203.246.112.137', 27017, 'seclab')
    collection = client.db['dynamic_testing_result']

    response = collection.find_one({"_id":md5})
    detected = response['detected']
    result_bc = response['result_bc']
    result_mc = response['result_mc']

    return detected, result_bc, result_mc