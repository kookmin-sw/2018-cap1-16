import boto3, time, os, shutil, zipfile
from settings import *

MALWARE_PATH = '/home/seclab/malwares/malware'
INSTANCE_MALWARE_PATH = ''
FTP_BASE_PATH = '/home/seclab/malwares/ftp_base'
REPORT_ZIP_PATH = '/home/seclab/malwares/report_zip'
REPORT_PATH = '/home/seclab/malwares/report'

INSTANCE_NUMBER = 20
MAX_MALWARE_PER_INSTANCE = 10000

error_instance_set = set()

# 인스턴스 목록 뽑아내기.
# Filters에 Values [] 안에 정규식을 넣어주면 걸러짐 현재 인스턴스 이름들은 capstone1, capstone2
def start_ec2(ec2, instances) :
    #인스턴스 시작 코드
    for instance in instances:
        print(instance['InstanceId'])
        ec2.start_instances(InstanceIds = [instance['InstanceId']])

    # 인스턴스 키는 시간(100sec) + 스타트업 스크립트 실행시간(3720sec)
    time.sleep(3820)

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
    global error_instance_set
    for i in range(INSTANCE_NUMBER) :
        dst_path = FTP_BASE_PATH + os.sep + str(i % INSTANCE_NUMBER)
        if not os.path.exists(dst_path) :
            os.makedirs(dst_path)

    for i, malware_path in enumerate(malware_path_list) :
        if i % INSTANCE_NUMBER in error_instance_set :
            continue
        malware_name = os.path.basename(malware_path)
        shutil.move(malware_path, FTP_BASE_PATH + os.sep + str(i % INSTANCE_NUMBER) + os.sep + malware_name)

    error_instance_set = set([i for i in range(INSTANCE_NUMBER)])

def unzip_report() :
    global error_instance_set
    for i in range(INSTANCE_NUMBER) :
        if os.path.exists(REPORT_ZIP_PATH + os.sep + str(i) + '.zip') :
            zip = zipfile.ZipFile(os.path.exists(REPORT_ZIP_PATH + os.sep + str(i) + '.zip'))
            zip.extractall(REPORT_PATH)
            zip.close()
            error_instance_set.remove(i)
    pass

def delete_malware() :
    for i in range(INSTANCE_NUMBER) :
        if i in error_instance_set :
            continue
        shutil.rmtree(FTP_BASE_PATH + os.sep + str(i))

def run() :
    while True :
        malware_path_list = create_malware_path_list(MALWARE_PATH)
        if len(malware_path_list) == 0 :
            break

        move_malware_to_ftp(malware_path_list)

        ec2 = boto3.client('ec2', region_name='ap-northeast-2', aws_access_key_id='', aws_secret_access_key='')
        instances = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['*']}])['Reservations'][0]['Instances']
        start_ec2(ec2, instances)
        stop_ec2(ec2, instances)
        unzip_report(instances)
        delete_malware()

if __name__ == '__main__' :
    run()
