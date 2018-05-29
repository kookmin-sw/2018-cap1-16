# acs 저장 경로
ACS_PATH = "API Call Seq 파일(acs)파일이 저장되어 있는 경로"
# fh_acs 저장 경로
FH_ACS_PATH = "acs파일의 feature vector를 저장할 경로"

# fops 저장 경로
FOPS_PATH = "funtion opcode seq(fops)파일이 저장되어 있는 경로 "
# fh_fops 저장 경로
FH_FOPS_PATH = "fops파일의 feature vecctor를 저장할 경로"

# CPU COUNT ( os.cpu_count() 미만으로 설정 )
CPU_COUNT = "사용할 CPU 코어 갯수"

# Feature Hashing 관련 상수 정의
# 최대 리스트 크기 ( 2 ^ k )
FEATURE_VECTOR_K = "Feature Vector 의 최대 크기 2 ^ k 형태로 표시"

MAX_LIST_SIZE = 1 << FEATURE_VECTOR_K
MOD_VALUE = MAX_LIST_SIZE -  1

# n-gram 시작
N_GRAM_START = "N gram 최소 크기"

# n-gram 끝
N_GRAM_END = "N gram 최대 크기"