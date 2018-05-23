import boto3, time, os, shutil, zipfile
from settings import *

MALWARE_PATH = '/home/seclab/malwares/malware'
INSTANCE_MALWARE_PATH = ''
FTP_BASE_PATH = '/home/seclab/malwares/ftp_base'
REPORT_ZIP_PATH = '/home/seclab/malwares/report_zip'
REPORT_PATH = '/home/seclab/malwares/report'

INSTANCE_NUMBER = 20
MAX_MALWARE_PER_INSTANCE = 10000
WAIT_TIME =  int(MAX_MALWARE_PER_INSTANCE * 0.55)

# 인스턴스 목록 뽑아내기.
# Filters에 Values [] 안에 정규식을 넣어주면 걸러짐 현재 인스턴스 이름들은 capstone1, capstone2
def start_ec2(ec2, instances) :
    #인스턴스 시작 코드
    for instance in instances:
        print(instance['InstanceId'])
        ec2.start_instances(InstanceIds = [instance['InstanceId']])

    # 인스턴스 키는 시간(100sec) + 스타트업 스크립트 실행시간(3720sec)
    time.sleep(WAIT_TIME)

def stop_ec2(ec2, instances) :
    # 인스턴스 스탑 코드
    for instance in instances:
        print(instance['InstanceId'])
        ec2.stop_instances(InstanceIds=[instance['InstanceId']])
    time.sleep(100)

def create_malware_path_list( path ) :
    malware_cnt = 0
    ret_list = []
    max_malware = MAX_MALWARE_PER_INSTANCE * INSTANCE_NUMBER
    for path, dirs, files in os.walk(path) :
        for file in files :
            malware_cnt += 1
            ret_list.append(os.path.join(path, file))
            if malware_cnt == max_malware :
                return ret_list
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
    for i in range(INSTANCE_NUMBER) :
        if os.path.exists(REPORT_ZIP_PATH + os.sep + str(i) + '.zip') :
            zip = zipfile.ZipFile(REPORT_ZIP_PATH + os.sep + str(i) + '.zip')
            zip.extractall(REPORT_PATH)
            zip.close()
        else :
            FTP_BASE_PATH + os.sep + str(i)
            for path, dirs, files in os.walk(FTP_BASE_PATH) :
                for file in files :
                    shutil.move(os.path.join(path, file), os.path.join(MALWARE_PATH, file))
    pass

def delete_malware() :
    for i in range(INSTANCE_NUMBER) :
        shutil.rmtree(FTP_BASE_PATH + os.sep + str(i))

def run() :
    global WAIT_TIME
    while True :
        malware_path_list = create_malware_path_list(MALWARE_PATH)
        if len(malware_path_list) == 0 :
            break
        WAIT_TIME = int(len(malware_path_list) / INSTANCE_NUMBER * 0.55)
        move_malware_to_ftp(malware_path_list)

        ec2 = boto3.client('ec2', region_name='ap-northeast-2', aws_access_key_id='', aws_secret_access_key='')
        instances = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['*']}])['Reservations'][0]['Instances']
        start_ec2(ec2, instances)
        stop_ec2(ec2, instances)
        unzip_report()
        delete_malware()

if __name__ == '__main__' :
    run()
