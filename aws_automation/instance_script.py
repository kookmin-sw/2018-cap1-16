import ftplib, os, socket, json, shutil, time
import settings

def connect():
	ftp = ftplib.FTP()
	ftp.connect(settings.FTP_HOST,settings.FTP_PORT)
	ftp.login(settings.ID,settings.PASSWD)
	return ftp

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

def get_file_list(ftp,remote_dir_path):
	ftp.cwd(remote_dir_path)
	return ftp.nlst()

def upload_files(ftp,local_dir_path,remote_dir_path):
	ftp.cwd(remote_dir_path)
	file_list = os.listdir(local_dir_path)
	for f in file_list:
		time.sleep(0.05)
		ftp.storbinary("STOR " + f ,open(os.path.join(local_dir_path,f),'rb'))

def make_zip(dir_path,zip_path):
	shutil.make_archive(zip_path,'zip',dir_path)

def run():
	ftp = connect()
	list_file = get_file_list(ftp,settings.remote_raw_path)
	
	for f in list_file:
		report = dict()
		md5 = os.path.splitext(f)[0]
		local_ip = get_ip_address()
		report['ip'] = local_ip
		out_file = open(settings.local_report_path+md5+'.json','w')
		json_report = json.dump(report,out_file)
		out_file.close()

	make_zip(settings.local_report_path,settings.local_zip_path)	
	upload_files(ftp,settings.local_zip_dir,settings.remote_zip_path)

if __name__ == '__main__':
	run()
