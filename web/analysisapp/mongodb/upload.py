from .connect import SeclabMongoClient
import sys, datetime
def upload_analysis_report(analysis_data):
    client = SeclabMongoClient('203.246.112.137', 27017, 'seclab')
    collection = client.db['analyzed_report']

    md5 = analysis_data['md5']
    if analysis_data['detected'] == 0:
        detected = False
    elif analysis_data['detected'] == 1:
        detected = True
    label = analysis_data['label']
    # ssdeep = analysis_data['SSDeep']
    # ssdeep_split = ssdeep.split(":")
    # ssdeep_chunk_size = ssdeep_split[0]
    # ssdeep_chunk = ssdeep_split[1]
    # ssdeep_double_chunk = ssdeep_split[2]
    collected_date = datetime.datetime.now()
    try:
        res = collection.insert({'_id': md5, "md5": md5, \
                           "detected": detected, 'label': label, \
                           # "SSDeep": ssdeep, "SSDeep_chunk_size":ssdeep_chunk_size,\
                           # "SSDeep_chunk":ssdeep_chunk,"SSDeep_double_chunk": ssdeep_double_chunk,\
                           "collected_date": collected_date})
    except:
        res = 0

    return res
