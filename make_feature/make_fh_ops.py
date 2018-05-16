import os, hashlib, pickle, sys

import multiprocessing as mp

from settings import *

def create_ops_list ( root ) :
    ret_list = []
    for path, dirs, files in os.walk(root) :
        for file in files :
            full_file_path = os.path.join(path, file)
            ext = os.path.splitext(full_file_path)[-1]
            if ext == '.ops' :
                ret_list.append(full_file_path)
    return ret_list

def make_fh( file_path ) :
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    sub_file_path = file_path.replace(OPS_PATH, '').replace(os.path.basename(file_path), '')

    fh_save_path = FH_OPS_PATH + sub_file_path

    if not os.path.exists(fh_save_path) :
        try :
            os.makedirs(fh_save_path)
        except :
            pass

    save_path = os.path.join(fh_save_path, file_name + '.fhops')

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
                index = hash_value % MAX_LIST_SIZE
                gram_fh_list[index] += 1
                for i in range(n, count_of_element) :
                    window = window[len(elements[i-n]):] + elements[i]
                    hash_value = int(hashlib.sha256(window.encode('utf-8')).hexdigest(), 16)
                    index = hash_value % MAX_LIST_SIZE
                    gram_fh_list[index] += 1
                max_value = max(gram_fh_list)
                min_value = min(gram_fh_list)
                if max_value - min_value == 0 :
                    fh_list += [ 0 for i in range(MAX_LIST_SIZE) ]
                else :
                    fh_list += [  (x - min_value) / (max_value - min_value) for x in gram_fh_list ]
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
    run()

