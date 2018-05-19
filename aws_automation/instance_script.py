import ftplib, os, socket, json, shutil, time

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

def make_zip(dir_path,zip_path):
    shutil.make_archive(zip_path,'zip',dir_path)

def run():
    ftp = connect()
    file_list = get_file_list(ftp,remote_raw_path)
    md5_list = [ os.path.splitext(file)[0] for file in file_list ]
    key_list = [ API_KEY_LIST[i % len(API_KEY_LIST)] for i in range(len(md5_list))]
    report_path_list = [ LOCAL_REPORT_PATH for i in range(len(md5_list)) ]
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        pool.starmap(vt.retrieving_file_scan_report, zip(file_list, report_path_list, key_list))
    make_zip( LOCAL_REPORT_PATH,local_zip_path)
    upload_files(ftp,local_zip_dir,remote_zip_path)
    shutil.rmtree( LOCAL_REPORT_PATH )
    shutil.rmtree(local_zip_dir)

if __name__ == '__main__':
    run()
