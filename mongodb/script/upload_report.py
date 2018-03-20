from connect import SeclabMongoClient
import os,datetime,json

DIRECTORY = '/home/jun/kisa_reports'

def upload_report(dir_url,collection):
	files = os.listdir(dir_url)
	file_count = len(files)
	remain_count = file_count
	for file in files:
		absolute_url = os.path.join(dir_url,file)
		with open(absolute_url,"r") as f:
			data = json.load(f)
			md5 = data['MD5']
			magic = data['Magic']
			sha1 = data['SHA-1']
			sha256 = data['SHA-256']
			filesize = int(data['File Size'])
			detected = data['detected']
			result = data['result']
			ssdeep = data['SSDeep']
			ssdeep_split = ssdeep.split(":")
			ssdeep_chunk_size = ssdeep_split[0]
			ssdeep_chunk = ssdeep_split[1]
			ssdeep_double_chunk = ssdeep_split[2]
			try:
				collection.insert({"_id":md5,"Magic":magic,\
					"File_Size":filesize,"SHA-1":sha1,"SHA-256":sha256,\
					"SSDeep": ssdeep, "SSDeep_chunk_size":ssdeep_chunk_size,\
					"SSDeep_chunk":ssdeep_chunk,"SSDeep_double_chunk": ssdeep_double_chunk,\
					"detected":detected,"result":result,\
					"Uploaded_Date":datetime.datetime.now()})
				print("%s is inserted (%d/%d) "%(md5,remain_count,file_count))
			except:
				print("%s is already in db (%d/%d) "%(md5,remain_count,file_count))

		remain_count -=1


if __name__ == '__main__':
	client = SeclabMongoClient('localhost',27017,'seclab')
	collection = client.db['analyzed_report']
	upload_report(DIRECTORY,collection)
