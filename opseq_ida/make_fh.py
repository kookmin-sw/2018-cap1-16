import os, subprocess, time, hashlib, pickle, sys

import multiprocessing as mp

from settings import *

def create_ops_list ( root ) :
    ret_list = []
    for file_path in os.listdir(root) :
        full_file_path = os.path.join(root, file_path)

        if os.path.isfile(full_file_path) :
            ext = os.path.splitext(full_file_path)[-1]
            if ext == '.ops' :
                ret_list.append(full_file_path)
    return ret_list

def make_fh( file_path ) :
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    save_path = os.path.join(FH_PATH, file_name + '.fh')

    if os.path.exists(save_path) :
        print("{}는 이미 분석 결과가 있습니다.".format(file_name))
        return
    with open(file_path, 'rb') as f :
        try :
            opcodes = pickle.load(f)
            count_of_opcode = len(opcodes)
            fh_list = []
            for n in range(N_GRAM_START, N_GRAM_END + 1) :
                gram_fh_list = [ 0 for i in range(MAX_LIST_SIZE) ]
                window = ''
                for i in range(n) :
                    window += opcodes[i]
                index = int(hashlib.md5(window.encode('utf-8')).hexdigest(), 16) % MAX_LIST_SIZE
                gram_fh_list[index] += 1
                for i in range(n, count_of_opcode) :
                    window = window[2:] + opcodes[i]
                    index = int(hashlib.md5(window.encode('utf-8')).hexdigest(), 16) % MAX_LIST_SIZE
                    gram_fh_list[index] += 1
                max_value = 0
                for each in gram_fh_list :
                    if max_value < each :
                        max_value = each
                if max_value == 0 :
                    fh_list += [ 0 for i in range(MAX_LIST_SIZE) ]
                else :
                    fh_list += [  x / max_value for x in gram_fh_list ]
        except :
            print("{}는 ops파일이 아닙니다.".format(file_path))
            print("{}을 분석하는데 실패하였습니다.".format(file_name))
            return

    with open(save_path, 'wb') as f :
        pickle.dump(fh_list, f)
        print("{}을 성공적으로 분석하였습니다.".format(file_name))


def run() :
    mp.freeze_support()
    ops_list=create_ops_list(OPS_PATH)
    print("Total OPS Count : {}".format(len(ops_list)))
    p = mp.Pool(CPU_COUNT)
    p.map(make_fh, ops_list)

if __name__ == '__main__' :
    if not os.path.exists(FH_PATH) :
        os.makedirs(FH_PATH)
    argv_cnt = len(sys.argv)
    if argv_cnt != 2 :
        print("make_fh.py")
        print("Opcode Sequence 추출 파일로 부터 Tensorflow Model 에 사용할 피쳐를 뽑는 코드")
        print("python make_fh.py <directory> : <directory> 하위에 있는 모든 파일(ops)에 대한 fh파일 추출" )
        print("python make_fh.py <file> : <file>에 대한 fh파일 추출")
    if argv_cnt == 2 :
        path = sys.argv[1]
        if os.path.isfile(path) :
            make_fh(path)
        elif os.path.isdir(path) :
            mp.freeze_support()
            file_list = create_ops_list(path)
            print("Total Malware Count : {}".format(len(file_list)))
            p = mp.Pool(CPU_COUNT)
            p.map(make_fh, file_list)
        else :
            print("존재하는 파일 혹은 폴더가 아닙니다.")