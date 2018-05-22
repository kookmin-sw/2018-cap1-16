import os, subprocess

import multiprocessing as mp
import sys

from settings import *

def create_file_list () :
    ret_list = []
    for path, dirs, files in os.walk(MALWARE_PATH) :
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
        return

    command = '"{ida_path}" -c -o"{idb_path}" -B -P+ "{malware_path}"'.format(ida_path=IDA_PATH, idb_path=dst_path, malware_path=file_path)

    try :
        subprocess.call(command, shell=True, timeout=TIME_OUT)
        if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb') :
            print("{}을 성공적으로 분석하였습니다.".format(file_name))
            os.remove(dst_path + '.asm')
        else :
            print("{}을 분석하는데 실패하였습니다.".format(file_name))
    except :
        print("{}을 분석하는데 실패하였습니다.".format(file_name))

def create_delete_vir_list() :
    ret_list = []
    for path, dirs, files in os.walk(IDB_PATH) :
        for file in files :
            ext = os.path.splitext(file)[-1]
            if ext == '.i64' :
                ret_list.append(os.path.join(path, file.replace('.i64', '.vir')))
            elif ext == '.idb' :
                ret_list.append(os.path.join(path, file.replace('.idb', '.vir')))
    return ret_list

def delete_file( file_path ) :
    os.remove(file_path)

def print_help() :
    print("make_idb.py")
    print("IDA Database 을 생성해주는 파이썬 스크립트")
    print("python make_idb.py <file> : <file>에 대해 idb(i64) 파일을 IDB_PATH에 생성")

if __name__ == '__main__' :
    if not os.path.exists(IDB_PATH) :
        os.makedirs(IDB_PATH)
    argv_cnt = len(sys.argv)
    if argv_cnt == 1 :
        mp.freeze_support()
        file_list = create_file_list()
        file_list.sort()
        print("Total Malware Count : {}".format(len(file_list)))
        p = mp.Pool(CPU_COUNT)
        p.map(make_idb, file_list)
        print("Delete Process Start")
        vir_list = create_delete_vir_list()
        p.map(delete_file, vir_list)
        print("Done")
    if argv_cnt == 2 :
        path = sys.argv[1]
        if os.path.isfile(path) :
            make_idb(path)
        else :
            print("존재하지 않는 파일입니다.")
    else :
        print_help()


