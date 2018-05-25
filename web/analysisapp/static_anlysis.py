import os,json,sys
from django.conf import settings

# import tensorflow script to system path
TENSOR_ROOT = os.path.join(settings.PROJECT_DIR, 'tensorflow_model')
sys.path.append(TENSOR_ROOT)
import testing_bc_static
import testing_mc_static

def run_static_analysis(upload_file_obj):

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
    cmd_run_ida_fh_fops = 'python ' + FEATURE_ROOT + os.sep + 'make_fh_fops.py ' + fops_file_path
    os.system(cmd_run_ida_fh_fops)

    result_bc = testing_bc_static.run(fh_fops_file_path)
    result_mc = testing_mc_static.run(fh_fops_file_path)

    return result_bc, result_mc
