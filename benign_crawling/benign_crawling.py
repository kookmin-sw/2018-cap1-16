import pefile, os, shutil, hashlib

import multiprocessing as mp

from settings import *

def get_file_path( root ) :
    path_32bit_exe, path_64bit_exe, path_32bit_dll, path_64bit_dll = [], [], [], []
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
            elif ext == '.dll' :
                try :
                    pe = pefile.PE(full_path)
                    machine_bit = pe.FILE_HEADER.Machine
                    if machine_bit == 0x014c:
                        print("32bit :", full_path)
                        path_32bit_dll.append(full_path)
                    elif machine_bit == 0x8664 or machine_bit == 0x0200:
                        print("64bit :", full_path)
                        path_64bit_dll.append(full_path)
                    else :
                        print("Error :", full_path)
                except :
                    pass
    return path_32bit_exe, path_64bit_exe, path_32bit_dll, path_64bit_dll

def get_file_md5( file_path, block_size = 8192 ) :
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f :
        buf = f.read(block_size)
        while buf :
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def crawling_32bit_exe( path_32bit ) :
    md5 = get_file_md5(path_32bit)
    target_path = os.path.join(DESTINATION_32_EXE_PATH, md5 + '.vir')
    if not os.path.exists(target_path) :
        try :
            shutil.copy(path_32bit, target_path)
        except :
            pass

def crawling_64bit_exe( path_64bit ) :
    md5 = get_file_md5(path_64bit)
    target_path = os.path.join(DESTINATION_64_EXE_PATH, md5 + '.vir')
    if not os.path.exists(target_path) :
        try :
            shutil.copy(path_64bit, target_path)
        except :
            pass


def crawling_32bit_dll( path_32bit ) :
    md5 = get_file_md5(path_32bit)
    target_path = os.path.join(DESTINATION_32_DLL_PATH, md5 + '.vir')
    if not os.path.exists(target_path) :
        try :
            shutil.copy(path_32bit, target_path)
        except :
            pass

def crawling_64bit_dll( path_64bit ) :
    md5 = get_file_md5(path_64bit)
    target_path = os.path.join(DESTINATION_64_DLL_PATH, md5 + '.vir')
    if not os.path.exists(target_path) :
        try :
            shutil.copy(path_64bit, target_path)
        except :
            pass

def run( root ) :
    mp.freeze_support()
    path_32bit_exe, path_64bit_exe, path_32bit_dll, path_64bit_dll = get_file_path( root )
    p = mp.Pool(os.cpu_count() // 2)
    print("Start copy 32bit EXE : {}".format(len(path_32bit_exe)))
    p.map(crawling_32bit_exe, path_32bit_exe)
    print("Start copy 64bit EXE: {}".format(len(path_64bit_exe)))
    p.map(crawling_64bit_exe, path_64bit_exe)
    print("Start copy 32bit DLL: {}".format(len(path_32bit_dll)))
    p.map(crawling_32bit_dll, path_32bit_dll)
    print("Start copy 64bit DLL: {}".format(len(path_64bit_dll)))
    p.map(crawling_64bit_dll, path_64bit_dll)
    print("Done")