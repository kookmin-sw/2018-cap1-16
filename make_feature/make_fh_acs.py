import os, hashlib, pickle, sys

import multiprocessing as mp

from settings import *

def create_acs_list ( root ) :
    ret_list = []
    for path, dirs, files in os.walk(root) :
        for file in files :
            full_file_path = os.path.join(path, file)
            ext = os.path.splitext(full_file_path)[-1]
            if ext == '.acs' :
                ret_list.append(full_file_path)
    return ret_list

def make_fh( file_path ) :
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    save_path =  FH_ACS_PATH + os.sep + file_name + '.fhacs'

    if os.path.exists(save_path) :
        print("{}는 이미 분석 결과가 있습니다.".format(file_name))
        return
    
    with open(file_path, 'rb') as f :
        try :
            elements = pickle.load(f)
            fh_list = []
            count_of_element = len(elements)
            if count_of_element < N_GRAM_END:
                return
            for n in range(N_GRAM_START, N_GRAM_END + 1) :
                gram_fh_list = [0 for i in range(MAX_LIST_SIZE)]
                window = ''
                for i in range(n) :
                    window += elements[i]
                hash_value = int(hashlib.sha256(window.encode('utf-8')).hexdigest(), 16)
                index = hash_value & MOD_VALUE
                gram_fh_list[index] += 1
                for i in range(n, count_of_element) :
                    window = window[len(elements[i-n]):] + elements[i]
                    hash_value = int(hashlib.sha256(window.encode('utf-8')).hexdigest(), 16)
                    index = hash_value & MOD_VALUE
                    gram_fh_list[index] += 1
                max_value = max(gram_fh_list)
                min_value = min(gram_fh_list)
                if max_value - min_value == 0 :
                    fh_list += [ 0 for i in range(MAX_LIST_SIZE) ]
                else :
                    fh_list += [  (x - min_value) / (max_value - min_value) for x in gram_fh_list ]
        except :
            print("{}는 acs파일이 아닙니다.".format(file_path))
            print("{}을 분석하는데 실패하였습니다.".format(file_name))
            return
    with open(save_path, 'wb') as f :
        pickle.dump(fh_list, f)
        print("{}을 성공적으로 분석하였습니다.".format(file_name))

def print_help():
    print("make_fh_acs.py")
    print("ACS 파일로 부터 Feature Vector를 생성 하는 코드")
    print("python make_idb_func_acs.py <file> : <file>에 대해 Feature Vector 생성해서 FH_ACS_PATH 에 저장")

if __name__ == '__main__':
    if os.path.exists(FH_ACS_PATH):
        os.makedirs(FH_ACS_PATH)
    argv_cnt = len(sys.argv)

    if argv_cnt == 1:
        mp.freeze_support()
        acs_list = create_acs_list(ACS_PATH)
        print("Total ACS Count : {}".format(len(acs_list)))
        p = mp.Pool(CPU_COUNT)
        p.map(make_fh, acs_list)

    elif argv_cnt == 2:
        path = sys.argv[1]
        if os.path.isfile(path):
            ext = os.path.splitext(path)[-1]
            if ext == '.acs':
                make_fh(path)
            else:
                print("ACS 파일이 아닙니다.")
        else:
            print("존재하는 파일 혹은 폴더가 아닙니다.")
    else:
        print_help()