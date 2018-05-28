# -*- coding: utf-8 -*-
import boto3, time, os, shutil, zipfile
import datetime
from settings import *

MALWARE_PATH = '/home/seclab/malwares/malware'
INSTANCE_MALWARE_PATH = ''
FTP_BASE_PATH = '/home/seclab/malwares/ftp_base'
REPORT_ZIP_PATH = '/home/seclab/malwares/report_zip'
REPORT_PATH = '/home/seclab/malwares/report'

INSTANCE_NUMBER = 20
MAX_MALWARE_PER_INSTANCE = 10000
WAIT_TIME =  int(MAX_MALWARE_PER_INSTANCE * 0.2)+100

# 인스턴스 목록 뽑아내기.
# Filters에 Values [] 안에 정규식을 넣어주면 걸러짐 현재 인스턴스 이름들은 capstone1, capstone2
def start_ec2(ec2, instances) :
    s = 0
    #인스턴스 시작 코드
    for instance in instances:
        try :
            ec2.start_instances(InstanceIds = [instance['InstanceId']])
            s += 1
        except :
            pass
    print("EC2 : {}".format(s))

    # 인스턴스 키는 시간(100sec) + 스타트업 스크립트 실행시간(3720sec)
    time.sleep(300)

def stop_ec2(ec2, instances) :
    # 인스턴스 스탑 코드
    for instance in instances:
        try :
            ec2.stop_instances(InstanceIds=[instance['InstanceId']])
        except :
            pass
    time.sleep(300)

def create_malware_path_list( path ) :
    malware_cnt = 0
    ret_list = []
    max_malware = MAX_MALWARE_PER_INSTANCE * INSTANCE_NUMBER
    for path, dirs, files in os.walk(path) :
        for file in files :
            if malware_cnt < max_malware :
                ret_list.append(os.path.join(path, file))
            malware_cnt += 1
    print("Total Malware : {}".format(malware_cnt))
    return ret_list

def move_malware_to_ftp( malware_path_list ) :
    for i in range(INSTANCE_NUMBER) :
        dst_path = FTP_BASE_PATH + os.sep + str(i)
        if not os.path.exists(dst_path) :
            os.makedirs(dst_path)
    for i, malware_path in enumerate(malware_path_list) :
        malware_name = os.path.basename(malware_path)
        shutil.move(malware_path, FTP_BASE_PATH + os.sep + str(i % INSTANCE_NUMBER) + os.sep + malware_name)

def unzip_report() :
    print("Unzip Start")
    ret = 0
    for i in range(INSTANCE_NUMBER) :
        if os.path.exists(REPORT_ZIP_PATH + os.sep + str(i) + '.zip') :
            ret += 1
            zip = zipfile.ZipFile(REPORT_ZIP_PATH + os.sep + str(i) + '.zip')
            zip.extractall(REPORT_PATH)
            zip.close()
            print("{} unzip".format(i))
            os.remove(REPORT_ZIP_PATH + os.sep + str(i) + '.zip')
        else :
            for path, dirs, files in os.walk(FTP_BASE_PATH + os.sep + str(i)) :
                for file in files :
                    shutil.move(os.path.join(path, file), os.path.join(MALWARE_PATH, file))
    print("Zip File : {}".format(ret))

def delete_malware() :
    print("Delete Malware")
    for i in range(INSTANCE_NUMBER) :
        shutil.rmtree(FTP_BASE_PATH + os.sep + str(i))

def report_cnt() :
    ret = 0
    for path, dirs, files in os.walk(REPORT_PATH) :
        for file in files :
            ext = os.path.splitext(file)[-1]
            if ext == '.json' :
                ret += 1
    return ret

def run() :
    global WAIT_TIME
    step = 1
    before = -1
    while True :
        print("Step : {}".format(step))
        print("Time : {}".format(datetime.datetime.now()))
        malware_path_list = create_malware_path_list(MALWARE_PATH)
        malware_cnt = len(malware_path_list)
        if len(malware_path_list) == 0 :
            print("분석이 완료 되었습니다.")
            break
        if before == malware_cnt :
            print("더이상 분석할 수 없습니다.")
            break
        before = malware_cnt
        print("Malware : {}".format(malware_cnt))
        WAIT_TIME = int(len(malware_path_list) / INSTANCE_NUMBER * 0.2)+100
        print("Wait Time :", WAIT_TIME)
        move_malware_to_ftp(malware_path_list)

        ec2 = boto3.client('ec2', region_name='us-west-2', aws_access_key_id='', aws_secret_access_key='')
        instances = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['*']}])['Reservations'][0]['Instances'] + ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['*']}])['Reservations'][1]['Instances']
        start_ec2(ec2, instances)
        time.sleep(WAIT_TIME)
        stop_ec2(ec2, instances)
        unzip_report()
        delete_malware()
        step += 1
        print("Report : {}".format(report_cnt()))

if __name__ == '__main__' :
    run()



