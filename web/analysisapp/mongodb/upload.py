from .client import MyMongoClient
import sys, datetime

def upload_static_testing_result(md5,result_bc,result_mc):
    client = MyMongoClient('203.246.112.137', 27017, 'seclab')
    collection = client.db['static_testing_result']
    result_mc = str(result_mc).replace('[',"").replace(']',"").replace(" ","")
    try:
        res = collection.insert({'_id': md5, "detected":result_bc[0], "result_bc":float("{0:.2f}".format(result_bc[1])), "result_mc":result_mc})

    except:
        res = collection.update({'_id': md5},{'$set':{"detected":result_bc[0], "result_bc":result_bc[1], "result_mc":result_mc}},upsert=True)

    return res

def upload_dynamic_testing_result(md5,result_bc,result_mc):
    client = MyMongoClient('203.246.112.137', 27017, 'seclab')
    collection = client.db['dynamic_testing_result']
    result_mc = str(result_mc).replace('[',"").replace(']',"").replace(" ","")
    try:
        res = collection.insert({'_id': md5, "detected":result_bc[0], "result_bc":float("{0:.2f}".format(result_bc[1])), "result_mc":result_mc})

    except:
        res = collection.update({'_id': md5},{'$set':{"detected":result_bc[0], "result_bc":result_bc[1], "result_mc":result_mc}},upsert=True)

    return res
