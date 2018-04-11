import sys, os
import learning_model, testing_model

def print_help() :
    print("ann_by_static.py")
    print("python ann_by_static.py -l : TRAIN_DATA_PATH 에 있는 파일을 학습합니다.")
    print("python ann_by_static.py -t <파일경로> : <파일경로>에 해당하는 파일에 대한 결과를 TEST_RESULT_PATH 에 저장합니다.")
if __name__ == '__main__' :
    argv_cnt = len(sys.argv)
    if argv_cnt == 2 :
        if sys.argv[1] == '-l' :
            learning_model.run()
        else :
            print_help()
    elif argv_cnt == 3 :
        if sys.argv[1] == '-t' :
            if os.path.isfile(sys.argv[2]) :
                testing_model.run(sys.argv[2])
            else :
                print("파일의 정보가 잘못 되었습니다.")
        else :
            print_help()
    else :
        print_help()
