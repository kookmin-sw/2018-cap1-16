import boto3, time, ftplib, os
from settings import *

def connect():
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST,FTP_PORT)
    ftp.login(ID,PASSWD)
    return ftp

# 인스턴스 목록 뽑아내기.
# Filters에 Values [] 안에 정규식을 넣어주면 걸러짐 현재 인스턴스 이름들은 capstone1, capstone2
ec2 = boto3.client('ec2', region_name='us-west-2',aws_access_key_id='', aws_secret_access_key='')
instances = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['capstone*']}])['Reservations'][0]['Instances']
print(len(instances))

#인스턴스 시작 코드
for instance in instances:
    print(instance['InstanceId'])
    ec2.start_instances(InstanceIds = [instance['InstanceId']])

# 인스턴스 키는 시간(100sec) + 스타트업 스크립트 실행시간(2000sec)
time.sleep(2100)

# 인스턴스 스탑 코드
for instance in instances:
    print(instance['InstanceId'])
    ec2.stop_instances(InstanceIds=[instance['InstanceId']])


# zip 파일이 다 모였는지 확인하는 부분 (미완성)
ftp = connect()
ftp.cwd(REMOTE_REPORT_PATH)
zip_list = ftp.nlst()
zip_num_list = [os.path.splitext(zip)[0] for zip in zip_list]
if not len(zip_num_list) == 24:
    required_list = [ str(i) for i in range(1,25)]
    remain_list = set(required_list) - set(zip_num_list)
    print(remain_list)