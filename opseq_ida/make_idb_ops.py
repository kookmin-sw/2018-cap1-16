import os, subprocess

import multiprocessing as mp

from settings import *

SCRIPT_PATH = os.path.join(IDA_PYTHON_SCRIPT_PATH, 'opcode.py')

def create_file_list ( root ) :
    ret_list = []
    for path, dirs, files in os.walk(root) :
        for file in files :
            ret_list.append(os.path.join(path, file))

    return ret_list

def make_idb( file_path ) :
    sub_file_path = os.path.split(file_path.replace(MALWARE_PATH, ''))[0]
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    idb_save_path = IDB_PATH + sub_file_path
    ops_save_path = OPS_PATH + sub_file_path

    if not os.path.exists(idb_save_path):
        os.makedirs(idb_save_path)

    if not os.path.exists(ops_save_path):
        os.makedirs(ops_save_path)

    dst_path = os.path.join(idb_save_path, file_name)
    ops_dst_path = os.path.join(ops_save_path, file_name) + '.ops'

    if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb') :
        return
    if os.path.exists(ops_dst_path):
        return
    command = '{ida_path} -c -o{idb_path} -A -S\"{script_path} {ops_path}\" -P+ {malware_path}'.format(ida_path=IDA_PATH, idb_path=dst_path, script_path = SCRIPT_PATH, ops_path = ops_dst_path, malware_path=file_path)
    try :
        subprocess.run(command)
        if os.path.exists(dst_path + '.i64') or os.path.exists(dst_path + '.idb') :
            pass
            #os.remove(file_path)
    except :
        pass


def run() :
    if not os.path.exists(IDB_PATH) :
        os.makedirs(IDB_PATH)
    mp.freeze_support()
    file_list=create_file_list(MALWARE_PATH)
    print("Total Malware Count : {}".format(len(file_list)))
    p = mp.Pool(CPU_COUNT)
    p.map(make_idb, file_list)