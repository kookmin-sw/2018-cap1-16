import os,json
from django.conf import settings

def run_static_analysis(upload_file_obj):

    IDA_ROOT = os.path.join(settings.PROJECT_DIR,'ida')
    FEATURE_ROOT = os.path.join(settings.PROJECT_DIR,'make_feature')
    TENSOR_ROOT = os.path.join(settings.PROJECT_DIR, 'tensorflow_model')

    upload_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)

    fops_folder_path = os.path.join(IDA_ROOT,'fops')
    fops_file_path = os.path.join(fops_folder_path,os.path.splitext(upload_file_obj.upload_file.name)[0]+'.fops')
    fh_fops_folder_path = os.path.join(FEATURE_ROOT,'fh_fops')
    fh_fops_file_path = os.path.join(fh_fops_folder_path,os.path.splitext(upload_file_obj.upload_file.name)[0]+'.fhfops')

    cmd_run_ida_fops = 'python ' + IDA_ROOT + os.sep + 'make_idb_fops.py ' + upload_file_path
    os.system(cmd_run_ida_fops)

    cmd_run_ida_fh_fops = 'python ' + FEATURE_ROOT + os.sep + 'make_fh_fops.py ' + fops_file_path
    os.system(cmd_run_ida_fh_fops)

    cmd_run_tensor_bc = 'python ' + TENSOR_ROOT + os.sep + 'testing_bc_static ' + fh_fops_file_path
    cmd_run_tensor_mc = 'python ' + TENSOR_ROOT + os.sep + 'testing_mc_static ' + fh_fops_file_path
    os.system(cmd_run_tensor_bc)
    os.system(cmd_run_tensor_mc)

    #static_analysis_json = open(static_analysis_json_path)
    ret_data = None
    return ret_data