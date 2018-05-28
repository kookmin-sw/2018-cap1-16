from .client import MyMongoClient
from .settings import *
import sys


def mongo_acs_search(md5):
    client = MyMongoClient(Host, Port , CukcooDB)
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
