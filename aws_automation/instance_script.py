import ftplib, os, socket, json, shutil, time, zipfile

import multiprocessing

import virustotal_public as vt

from settings import *

def connect():
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST,FTP_PORT)
    ftp.login(ID,PASSWD)
    return ftp

def get_file_list(ftp,remote_dir_path):
    ftp.cwd(remote_dir_path)
    return ftp.nlst()

def upload_files(ftp,local_dir_path,remote_dir_path):
    ftp.cwd(remote_dir_path)
    file_list = os.listdir(local_dir_path)
    for f in file_list:
        time.sleep(INTERVAL_TIME)
        ftp.storbinary("STOR " + f ,open(os.path.join(local_dir_path,f),'rb'))

def make_zip():
    if not os.path.exists(LOCAL_ZIP_PATH) :
        os.makedirs(LOCAL_ZIP_PATH)
    zip = zipfile.ZipFile(LOCAL_ZIP_PATH + os.sep + INSTANCE_NUM + '.zip', 'w')
    for path, dirs, files in os.walk(LOCAL_REPORT_PATH ):
        for file in files:
            zip.write(os.path.join(path, file), file, compress_type=zipfile.ZIP_DEFLATED)
    zip.close()

def run():
    start_time =time.time()
    shutil.rmtree(LOCAL_REPORT_PATH, ignore_errors=True)
    ftp = connect()
    file_list = get_file_list(ftp,REMOTE_FILE_PATH)
    md5_list = [ os.path.splitext(file)[0] for file in file_list ]
    while len(md5_list) != 0 :
        key_list = [ API_KEY_LIST[i % len(API_KEY_LIST)] for i in range(len(md5_list))]
        report_path_list = [ LOCAL_REPORT_PATH for i in range(len(md5_list)) ]
        if not os.path.exists(LOCAL_REPORT_PATH):
            os.makedirs(LOCAL_REPORT_PATH)

        with multiprocessing.Pool(os.cpu_count()) as pool:
            pool.starmap(vt.retrieving_file_scan_report, zip(md5_list, report_path_list, key_list))

        json_list = os.listdir(LOCAL_REPORT_PATH)
        json_md5_list = [ os.path.splitext(json_path)[0] for json_path in json_list ]
        md5_list = list( set(md5_list) - set(json_md5_list) )

    make_zip()
    ftp = connect()
    upload_files(ftp,LOCAL_ZIP_DIR,REMOTE_REPORT_PATH)
    shutil.rmtree( LOCAL_REPORT_PATH )
    shutil.rmtree(LOCAL_ZIP_DIR)
    print(time.time()-start_time)
if __name__ == '__main__':
    run()
