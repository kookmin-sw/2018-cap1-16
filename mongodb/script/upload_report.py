from connect import SeclabMongoClient
import os,datetime,json

DIRECTORY = '/home/seclab/sample_report'

def upload_report(dir_url,collection):
	files = os.listdir(dir_url)
	file_count = len(files)
	remain_count = file_count
	for file in files:
		absolute_url = os.path.join(dir_url,file)
		with open(absolute_url,"r") as f:
			data = json.load(f)
			md5 = data['md5']
			if data['detected'] == 0:
				detected = False
			elif data['detected'] == 1:
				detected = True
			label = data['label']
			#ssdeep = data['SSDeep']
			#ssdeep_split = ssdeep.split(":")
			#ssdeep_chunk_size = ssdeep_split[0]
			#ssdeep_chunk = ssdeep_split[1]
			#ssdeep_double_chunk = ssdeep_split[2]
			collected_date=datetime.datetime.now()
			try:
				collection.insert({'_id':md5,"md5":md5,\
					"detected":detected,'label':label,\
					#"SSDeep": ssdeep, "SSDeep_chunk_size":ssdeep_chunk_size,\
					#"SSDeep_chunk":ssdeep_chunk,"SSDeep_double_chunk": ssdeep_double_chunk,\
					"collected_date":collected_date})
				print("%s is inserted (%d/%d) "%(md5,remain_count,file_count))
			except:
				try:
					collection.update({"md5": md5}, {'$set': {"md5":md5,"label": label, "detected":detected,\
										"collected_date": collected_date}}, upsert=True)
					print("%s is updated (%d/%d) " % (md5, remain_count, file_count))
				except:
					print("update %s throws error! So Skipped! (%d/%d) " % (md5, remain_count, file_count))
		remain_count -=1


if __name__ == '__main__':
	client = SeclabMongoClient('203.246.112.137',27017,'seclab')
	collection = client.db['analyzed_report']
	upload_report(DIRECTORY,collection)
