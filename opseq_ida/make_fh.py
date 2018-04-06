import os, subprocess, time, hashlib, pickle

import multiprocessing as mp

from settings import *

def create_ops_list ( root ) :
    ret_list = []
    for path, dirs, files in os.walk(root) :
        for file in files :
            ret_list.append(os.path.join(path, file))
    return ret_list

def make_fh( file_path ) :
    sub_file_path = os.path.split(file_path.replace(OPS_PATH, ''))[0]
    file_name = os.path.splitext(os.path.basename(file_path))[0] + '.ifh'
    save_path = FH_PATH + sub_file_path
    if not os.path.exists(save_path) :
        os.makedirs(save_path)
    full_save_path = os.path.join(save_path, file_name)
    if os.path.exists(full_save_path) :
        return
    with open(file_path, 'r') as f :
        opcodes = [ x.strip() for x in f.readlines() ]
        count_of_opcode = len(opcodes)
        if count_of_opcode < 5 :
            return
        fh_list = []
        for n in range(N_GRAM_START, N_GRAM_END + 1) :
            gram_fh_list = [ 0 for i in range(MAX_LIST_SIZE) ]
            window = ''
            for i in range(n) :
                window += opcodes[i]
            index = int(hashlib.md5(window.encode('utf-8')).hexdigest(), 16) % MAX_LIST_SIZE
            dicision = int(hashlib.sha256(window.encode('utf-8')).hexdigest(), 16) % 2
            if dicision == 1 and gram_fh_list[index] != BOUNDARY_SIZE:
                gram_fh_list[index] += 1
            elif dicision == 0 and gram_fh_list[index] != -BOUNDARY_SIZE :
                gram_fh_list[index] -= 1
            for i in range(n, count_of_opcode) :
                window = window[2:] + opcodes[i]
                index = int(hashlib.md5(window.encode('utf-8')).hexdigest(), 16) % MAX_LIST_SIZE
                dicision = int(hashlib.sha256(window.encode('utf-8')).hexdigest(), 16) % 2
                if dicision == 1 and gram_fh_list[index] != BOUNDARY_SIZE:
                    gram_fh_list[index] += 1
                elif dicision == 0 and gram_fh_list[index] != -BOUNDARY_SIZE:
                    gram_fh_list[index] -= 1
            fh_list += [ x / BOUNDARY_SIZE  for x in gram_fh_list ]

    with open(full_save_path, 'wb') as f :
        pickle.dump(fh_list, f)

def run() :
    mp.freeze_support()
    ops_list=create_ops_list(OPS_PATH)
    print("Total OPS Count : {}".format(len(ops_list)))
    p = mp.Pool(CPU_COUNT)
    p.map(make_fh, ops_list)
