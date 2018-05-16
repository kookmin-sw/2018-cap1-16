import os

# acs 저장 경로
ACS_PATH = os.path.normpath(os.path.abspath('./acs'))
# fh_acs 저장 경로
FH_ACS_PATH = os.path.normpath(os.path.abspath('./fh_acs'))

# fops 저장 경로
FOPS_PATH = os.path.normpath(os.path.abspath('./fops'))
# fh_fops 저장 경로
FH_FOPS_PATH = os.path.normpath(os.path.abspath('./fh_fops'))

# ops 저장 경로
OPS_PATH = os.path.normpath(os.path.abspath('./ops'))
# fh_ops 저장 경로
FH_OPS_PATH = os.path.normpath(os.path.abspath('./fh_ops'))

# CPU COUNT
CPU_COUNT = 4

# Feature Hashing 관련 상수 정의
# 최대 리스트 크기
MAX_LIST_SIZE = 4096

# n-gram 시작
N_GRAM_START = 3

# n-gram 끝
N_GRAM_END = 5