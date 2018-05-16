import os, subprocess, sys

import multiprocessing as mp

from settings import *

SCRIPT_PATH = os.path.join(IDA_PYTHON_SCRIPT_PATH, 'opcode.py')

def create_idb_list ( root ) :
    ret_list = []
    for path, dirs, files in os.walk(root) :
        for file in files :
            ext = os.path.splitext(file)[-1]
            if ext == '.i64' or ext == '.idb' :
                ret_list.append(os.path.join(path, file))
    return ret_list

def make_ops( file_path ) :
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    sub_file_path = file_path.replace(IDB_PATH,'').replace(os.path.basename(file_path), '')

    ops_save_path = OPS_PATH + sub_file_path

    if not os.path.exists(ops_save_path):
        os.makedirs(ops_save_path)

    ops_dst_path = os.path.join(ops_save_path, file_name) + '.ops'

    if os.path.exists(ops_dst_path) :
        return

    command = '"{ida_path}" -A -S"{script_path} {ops_path}" "{idb_path}"'.format(ida_path=IDA_PATH, script_path = SCRIPT_PATH, ops_path = ops_dst_path, idb_path=file_path)

    subprocess.run(command)

if __name__ == '__main__' :
    if not os.path.exists(OPS_PATH) :
        os.makedirs(OPS_PATH)
    argv_cnt = len(sys.argv)
    if argv_cnt != 2 :
        print("make_ops.py")
        print("IDA Database 파일로 부터 Opcode Sequence를 추출하는 코드")
        print("python make_ops.py <directory> : <directory> 하위에 있는 모든 idb(i64) 파일로부터 ops파일을 추출" )
        print("python make_ops.py <file> : <file>에서 ops파일을 추출")
    if argv_cnt == 2 :
        path = sys.argv[1]
        if os.path.isfile(path) :
            ext = os.path.splitext(path)[-1]
            if ext == '.i64' or ext == '.idb' :
                make_ops(path)
            else :
                print("IDB 파일이 아닙니다.")
        elif os.path.isdir(path) :
            mp.freeze_support()
            file_list = create_idb_list(path)
            print("Total IDB Count : {}".format(len(file_list)))
            p = mp.Pool(CPU_COUNT)
            p.map(make_ops, file_list)
        else :
            print("존재하는 파일 혹은 폴더가 아닙니다.")