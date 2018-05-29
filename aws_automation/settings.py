import os

# FTP Setting
FTP_HOST = 'YOUR_FTP_HOST(IP)'
FTP_PORT = 'FTP_PORT(21)'
ID = 'FTP_ID'
PASSWD = 'FTP_PASSWORD'

# INSTANCE Number ( 반드시 문자열 구조 ex '1' )
INSTANCE_NUM = 'INSTANCE_NUM'

# Virus Total 분석이 필요한 파일이 저장되어 있는 경로
REMOTE_FILE_BASE_PATH = 'FTP_BASE_PATH'
REMOTE_FILE_PATH = os.path.join(REMOTE_FILE_BASE_PATH, INSTANCE_NUM)

# 리포트를 저장할 FTP 위치
REMOTE_REPORT_PATH = 'REMOTE_REPORT_PATH'

# 인스턴스에서 리포트 및 리포트를 압축한 파일을 저장할 위치
LOCAL_REPORT_PATH = 'LOCAL_REPORT_PATH'
LOCAL_ZIP_DIR = 'LOCAL_REPORT_ZIP_PATH'

# Interval Time
INTERVAL_TIME = 0.05

# Virus Total API Key List
API_KEY_LIST = [
]