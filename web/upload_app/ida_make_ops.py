import os, subprocess
import multiprocessing as mp

from .ida_settings import *

SCRIPT_PATH = os.path.join(IDA_PYTHON_SCRIPT_PATH, 'opcode.py')

def make_ops( file_path ) :
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    idb_save_path = IDB_PATH
    ops_save_path = OPS_PATH
    dst_path = os.path.join(idb_save_path, file_name)
    ops_dst_path = os.path.join(ops_save_path, file_name) + '.ops'

    if os.path.exists(ops_dst_path):
        return ops_dst_path

    command = '{ida_path} -c -o{idb_path} -A -S\"{script_path} {ops_path}\" -P+ {malware_path}'.format(ida_path=IDA_PATH, idb_path=dst_path, script_path = SCRIPT_PATH, ops_path = ops_dst_path, malware_path=file_path)
    try :
        subprocess.run(command)
        if os.path.exists(ops_dst_path):
            return ops_dst_path
    except :
        pass


#def run(file_path) :
    #mp.freeze_support()
    #print("Total Malware Count : {}".format(len(file_list)))
    #p = mp.Pool(CPU_COUNT)
    #p.map(make_idb, file_path)