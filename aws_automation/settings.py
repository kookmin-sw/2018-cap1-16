import datetime
# FTP Setting
FTP_HOST = '203.246.112.137'
FTP_PORT = 2221
ID = 'seclab'
PASSWD = 'seclab4680'

# INSTANCE Number
INSTANCE_NUM = '1'

# ??
REMOTE_FILE_PATH = '/home/seclab/malwares/test/'+ INSTANCE_NUM
REMOTE_REPORT_PATH = '/home/seclab/malwares/report/'

# ??
LOCAL_REPORT_PATH = '/home/ubuntu/report/'
LOCAL_ZIP_DIR = '/home/ubuntu/zip'
LOCAL_ZIP_PATH = '/home/ubuntu/zip/'+str(datetime.datetime.now())+'_'+INSTANCE_NUM

# Interval Time
INTERVAL_TIME = 0.05

# Virus Total API Key List
API_KEY_LIST = [
]