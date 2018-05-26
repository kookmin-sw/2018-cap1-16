import os,json,sys
from django.conf import settings

from tensorflow_model import testing_bc_static
from tensorflow_model import testing_mc_static
from pefile_viewer import peview

def run_static_testing(upload_file_obj):

    IDA_ROOT = os.path.join(settings.PROJECT_DIR,'ida')
    FEATURE_ROOT = os.path.join(settings.PROJECT_DIR,'make_feature')

    upload_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)
    file_name = os.path.splitext(upload_file_obj.upload_file.name)[0]

    fops_folder_path = os.path.join(IDA_ROOT,'fops')
    fops_file_path = os.path.join(fops_folder_path,file_name+'.fops')
    cmd_run_ida_fops = 'python ' + IDA_ROOT + os.sep + 'make_idb_fops.py ' + upload_file_path
    os.system(cmd_run_ida_fops)

    fh_fops_folder_path = os.path.join(FEATURE_ROOT,'fh_fops')
    fh_fops_file_path = os.path.join(fh_fops_folder_path,file_name+'.fhfops')
    cmd_fh_fops = 'python ' + FEATURE_ROOT + os.sep + 'make_fh_fops.py ' + fops_file_path
    os.system(cmd_fh_fops)

    result_bc = testing_bc_static.run(fh_fops_file_path)
    result_mc = testing_mc_static.run(fh_fops_file_path)

    return result_bc, result_mc


def run_pefile_viewer(upload_file_obj):
    upload_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)
    peviewer = peview.Peview(upload_file_path)
    total_report = dict()

    # hash_info
    hash_report = dict()
    hashes = peviewer.get_hash()
    hash_report['md5'] = hashes[0]
    hash_report['sha1'] = hashes[1]
    hash_report['sha256'] = hashes[2]
    hash_report['imp_hash'] = hashes[3]
    total_report['hash'] = hash_report



    return total_report