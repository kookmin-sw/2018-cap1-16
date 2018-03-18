from connect import MyMongoClient
import os,datetime,json

DIRECTORY = '/home/jun/similarity_files_report'

def upload_report(dir_url,collection):
	files = os.listdir(dir_url)
	file_count = len(files)
	remain_count = file_count
	for file in files:
		absolute_url = os.path.join(dir_url,file)
		with open(absolute_url,"r") as f:
			data = json.load(f)
			md5 = data['MD5']
			ssdeep = data['SSDeep']
			ssdeep_split = ssdeep.split(":")
			ssdeep_chunk_size = ssdeep_split[0]
			ssdeep_chunk = ssdeep_split[1]
			ssdeep_double_chunk = ssdeep_split[2]
			try:
				collection.insert({"_id":md5,\
					"SSDeep": ssdeep, "SSDeep_chunk_size":ssdeep_chunk_size,\
					"SSDeep_chunk":ssdeep_chunk,\
					"SSDeep_double_chunk": ssdeep_double_chunk})
				print("%s is inserted (%d/%d) "%(md5,remain_count,file_count))
			except:
				print("%s is already in db (%d/%d) "%(md5,remain_count,file_count))

		remain_count -=1


if __name__ == '__main__':
	client = MyMongoClient('localhost',27017,'seclab')
	collection = client.db['ssdeep_report']
	upload_report(DIRECTORY,collection)