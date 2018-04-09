from .connect import SeclabMongoClient
import sys
def md5_search(md5):
    client = SeclabMongoClient('203.246.112.131', 27017, 'seclab')
    collection = client.db['analyzed_report']
    res = collection.find_one({"_id": md5})
    return res

    if res is not 0 :
        return res
    else:
        return 0