import os,sys, shutil, pickle
from django.conf import settings
from .mongodb.search import mongo_acs_search

# import cuckoo script to system path
CUCKOO_SCRIPT_ROOT = os.path.join(os.path.join(settings.PROJECT_DIR,'cuckoo'),'scripts')
sys.path.append(CUCKOO_SCRIPT_ROOT)
import upload_file

# run dynamic analysis
def run_dynamic_analysis(upload_file_obj):

    upload_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)
    dynamic_analysis_data = upload_file.run(upload_file_path)

    return dynamic_analysis_data

# test dynamic classification
def test_dynamic_clasification(md5):

    # get Api Call Sequence by searching mongoDB
    acs_list = mongo_acs_search(md5)

    # Feature Hash and Tensorflow Directory
    FEATURE_ROOT = os.path.join(settings.PROJECT_DIR, 'make_feature')
    TENSOR_ROOT = os.path.join(settings.PROJECT_DIR, 'tensorflow_model')

    # make md5.acs file
    acs_folder_path = os.path.join(FEATURE_ROOT, 'acs')
    acs_file_path = os.path.join(acs_folder_path,md5+'.acs')
    if not os.path.exists(acs_folder_path):
        os.makedirs(acs_folder_path)
    with open(acs_file_path,'wb') as f:
        if (len(acs_list) >= 5):
            pickle.dump(acs_list, f)
    f.close()

    # make 'run feature Hash' command
    cmd_ida_fh_acs = 'python ' + FEATURE_ROOT + os.sep + 'make_fh_acs.py ' + acs_file_path
    os.system(cmd_ida_fh_acs)
    # make fh_acs file path
    fh_acs_file_path = os.path.join(os.path.join(FEATURE_ROOT, 'fh_acs'),md5+'.fhacs')

    # make 'run bc&mc test' command
    cmd_tensor_bc = 'python ' + TENSOR_ROOT + os.sep + 'testing_bc_dynamic.py ' + fh_acs_file_path
    cmd_tensor_mc = 'python ' + TENSOR_ROOT + os.sep + 'testing_mc_dynamic.py ' + fh_acs_file_path
    os.system(cmd_tensor_bc)
    os.system(cmd_tensor_mc)

    # remove the temp file
    shutil.rmtree(acs_folder_path)

    result_bc, result_mc = None, None
    return result_bc, result_mc