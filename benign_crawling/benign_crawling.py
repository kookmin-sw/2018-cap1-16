import pefile, os, shutil, hashlib

import multiprocessing as mp

from benign_crawling.settings import *

def get_file_path( root ) :
    path_32bit_exe, path_64bit_exe = [], []
    for path, dirs, files in os.walk(root) :
        for file in files :
            ext = os.path.splitext(file)[-1]
            full_path = os.path.join(path, file)
            if ext == '.exe' :
                try :
                    pe = pefile.PE(full_path)
                    machine_bit = pe.FILE_HEADER.Machine
                    if machine_bit == 0x014c:
                        print("32bit :", full_path)
                        path_32bit_exe.append(full_path)
                    elif machine_bit == 0x8664 or machine_bit == 0x0200:
                        print("64bit :", full_path)
                        path_64bit_exe.append(full_path)
                    else :
                        print("Error :", full_path)
                except :
                    pass
    return path_32bit_exe, path_64bit_exe

def get_file_md5( file_path, block_size = 8192 ) :
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f :
        buf = f.read(block_size)
        while buf :
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def crawling_32bit( path_32bit ) :
    md5 = get_file_md5(path_32bit)
    print(md5, path_32bit)
    if not os.path.exists(path_32bit) :
        try :
            shutil.copy(path_32bit, os.path.join(DESTINATION_32_PATH, md5 + '.vir'))
        except :
            pass

def crawling_64bit( path_64bit ) :
    md5 = get_file_md5(path_64bit)
    print(path_64bit)
    if not os.path.exists(path_64bit) :
        try :
            shutil.copy(path_64bit, os.path.join(DESTINATION_64_PATH, md5 + '.vir'))
        except :
            pass

def run( root ) :
    mp.freeze_support()
    path_32bit_exe, path_64bit_exe = get_file_path( root )
    p = mp.Pool(os.cpu_count() // 2)
    p.map(crawling_32bit, path_32bit_exe)
    p.map(crawling_64bit, path_64bit_exe)