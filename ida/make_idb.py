import os, subprocess

import multiprocessing as mp
import sys

from settings import *

SCRIPT_PATH = os.path.join(IDA_PYTHON_SCRIPT_PATH, 'opcode.py')

def create_file_list ( root ) :
    ret_list = []
    for path, dirs, files in os.walk(root) :
        for file in files :
            full_file_path = os.path.join(path, file)
            ret_list.append(full_file_path)
    return ret_list

def make_idb( file_path ) :
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    sub_file_path = file_path.replace(MALWARE_PATH,'').replace(os.path.basename(file_path), '')

    idb_save_path = IDB_PATH + sub_file_path

    if not os.path.exists(idb_save_path):
        os.makedirs(idb_save_path)

    dst_path = os.path.join(idb_save_path, file_name)
    if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb') :
        print("{}는 이미 분석결과가 존재 합니다.".format(file_name))
        os.remove(file_path)
        return

    command = '"{ida_path}" -c -o"{idb_path}" -B -P+ "{malware_path}"'.format(ida_path=IDA_PATH, idb_path=dst_path, malware_path=file_path)
    try :
        subprocess.run(command)
        if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb') :
            print("{}을 성공적으로 분석하였습니다.".format(file_name))
            #os.remove(dst_path + '.asm')
            #os.remove(file_path)
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
        print("make_idb.py")
        print("IDA Database 을 생성해주는 파이썬 스크립트")
        print("python make_idb.py <directory> : <directory> 하위에 있는 모든 파일에 대한 idb(i64) 파일 생성" )
        print("python make_idb.py <file> : <file>에 대해 idb(i64) 파일 생성")
    if argv_cnt == 2 :
        path = sys.argv[1]
        if os.path.isfile(path) :
            make_idb(path)
        elif os.path.isdir(path) :
            mp.freeze_support()
            file_list = create_file_list(path)
            print("Total Malware Count : {}".format(len(file_list)))
            p = mp.Pool(CPU_COUNT)
            p.map(make_idb, file_list)
            print("Done")			
        else :
            print("존재하는 파일 혹은 폴더가 아닙니다.")


