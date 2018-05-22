import os, subprocess

import multiprocessing as mp
import sys

from settings import *

SCRIPT_PATH = os.path.join(IDA_PYTHON_SCRIPT_PATH, 'fopcode.py')

def create_file_list () :
    ret_list = []
    for path, dirs, files in os.walk(MALWARE_PATH) :
        for file in files :
            full_file_path = os.path.join(path, file)
            ret_list.append(full_file_path)
    return ret_list
def make_idb_fops( file_path ) :
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    sub_file_path = file_path.replace(MALWARE_PATH, '').replace(os.path.basename(file_path), '')

    idb_save_path = IDB_PATH + sub_file_path
    fops_save_path = FOPS_PATH + sub_file_path

    if not os.path.exists(idb_save_path):
        os.makedirs(idb_save_path)

    if not os.path.exists(fops_save_path):
        os.makedirs(fops_save_path)

    dst_path = os.path.join(idb_save_path, file_name)
    fops_dst_path = os.path.join(fops_save_path, file_name) + '.fops'

    if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb') or os.path.exists(fops_dst_path):
        return

    command = '"{ida_path}" -c -o"{idb_path}" -A -S"{script_path} {fops_path}" -P+ "{malware_path}"'.format(ida_path=IDA_PATH, idb_path=dst_path, script_path=SCRIPT_PATH, fops_path=fops_dst_path, malware_path=file_path)
    try:
        subprocess.call(command, shell=True, timeout=TIME_OUT)
        if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb'):
            print("{}을 성공적으로 분석하였습니다.".format(file_name))
        else:
            print("{}을 분석하는데 실패하였습니다.".format(file_name))
    except:
        print("{}을 분석하는데 실패하였습니다.".format(file_name))

def print_help() :
    print("make_idb_fops.py")
    print("IDA Database 파일과 함수별 Opcode Sequence를 생성해주는 파이썬 스크립트")
    print("python make_idb_func_fops.py <file> : <file>에 대해 idb(i64) 파일과 fops파일을 추출해 IDB_PATH 와 FOPS_PATH 로 저장")

if __name__ == '__main__' :
    argv_cnt = len(sys.argv)
    if argv_cnt == 1 :
        mp.freeze_support()
        file_list = create_file_list()
        print("Total Malware Count : {}".format(len(file_list)))
        p = mp.Pool(CPU_COUNT)
        p.map(make_idb_fops, file_list)

    if argv_cnt == 2 :
        path = sys.argv[1]
        if os.path.isfile(path) :
            make_idb_fops(path)
        else :
            print("존재하는 파일 혹은 폴더가 아닙니다.")
    else :
        print_help()


