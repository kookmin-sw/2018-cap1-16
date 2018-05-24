import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# IDA 경로
IDA_PATH = os.path.normpath('C:/Program Files/IDA 7.0/idat64.exe')

# malware 경로
MALWARE_PATH = os.path.normpath(os.path.abspath('./malware'))

# ZIP FILE PATH
ZIP_FILE_PATH = os.path.normpath(os.path.abspath('./zipfile'))

# idb(i64) 저장 경로
IDB_PATH = os.path.join(BASE_DIR,'idb')

# ops 저장 경로
OPS_PATH = os.path.normpath(os.path.abspath('./ops'))

# fops 저장 경로
FOPS_PATH = os.path.join(BASE_DIR,'fops')

# ida python script 저장 경로
IDA_PYTHON_SCRIPT_PATH = os.path.join(BASE_DIR,'ida_script')

# CPU COUNT
CPU_COUNT = 4

# TIME OUT
TIME_OUT = 60