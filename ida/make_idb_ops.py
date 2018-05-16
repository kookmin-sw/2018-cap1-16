import os, subprocess

import multiprocessing as mp
import sys

from settings import *

SCRIPT_PATH = os.path.join(IDA_PYTHON_SCRIPT_PATH, 'opcode.py')

def make_idb_ops( file_path ) :
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    sub_file_path = file_path.replace(MALWARE_PATH,'').replace(os.path.basename(file_path), '')

    idb_save_path = IDB_PATH + sub_file_path
    ops_save_path = OPS_PATH + sub_file_path

    if not os.path.exists(idb_save_path):
        os.makedirs(idb_save_path)

    if not os.path.exists(ops_save_path):
        os.makedirs(ops_save_path)

    dst_path = os.path.join(idb_save_path, file_name)
    ops_dst_path = os.path.join(ops_save_path, file_name) + '.ops'

    if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb') or os.path.exists(ops_dst_path):
        return

    command = '"{ida_path}" -c -o"{idb_path}" -A -S"{script_path} {ops_path}" -P+ "{malware_path}"'.format(ida_path=IDA_PATH, idb_path=dst_path, script_path=SCRIPT_PATH, ops_path=ops_dst_path,malware_path=file_path)
    try :
        subprocess.run(command)
        if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb') :
            print("{}을 성공적으로 분석하였습니다.".format(file_name))
            os.remove(file_path)
        else :
            print("{}을 분석하는데 실패하였습니다.".format(file_name))
    except :
        print("{}을 분석하는데 실패하였습니다.".format(file_name))

if __name__ == '__main__' :
    if not os.path.exists(IDB_PATH) :
        os.makedirs(IDB_PATH)
    if not os.path.exists(OPS_PATH) :
        os.makedirs(OPS_PATH)
    argv_cnt = len(sys.argv)
    if argv_cnt != 2 :
        print("make_idb_ops.py")
        print("IDA Database 파일과 Opcode Sequence를 생성해주는 파이썬 스크립트")
        print("python make_idb_ops.py <directory> : <directory> 하위에 있는 모든 파일에 대한 idb(i64) 파일과 ops파일을 추출" )
        print("python make_idb_ops.py <file> : <file>에 대해 idb(i64) 파일과 ops파일을 추출")
    if argv_cnt == 2 :
        path = sys.argv[1]
        if os.path.isfile(path) :
            make_idb_ops(path)
        elif os.path.isdir(path) :
            mp.freeze_support()
            file_list = create_file_list(path)
            print("Total Malware Count : {}".format(len(file_list)))
            p = mp.Pool(CPU_COUNT)
            p.map(make_idb_ops, file_list)
        else :
            print("존재하는 파일 혹은 폴더가 아닙니다.")


