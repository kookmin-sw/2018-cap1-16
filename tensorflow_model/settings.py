import os

# 정적  이진 Check Point 위치
STATIC_BC_CHECK_POINT = os.path.normpath(os.path.abspath('./static_bc_model.ckpt'))

# 정적 멀티 Check Point 위치
STATIC_MC_CHECK_POINT = os.path.normpath(os.path.abspath('./static_mc_model.ckpt'))

# 정적 분석 학습 파일 위치
TRAIN_STATIC_DATA_PATH = os.path.normpath(os.path.abspath('./train_static_data'))

# 학습에 사용할 라벨
TRAIN_LABEL_PATH = os.path.normpath(os.path.abspath('./train_data.csv'))

