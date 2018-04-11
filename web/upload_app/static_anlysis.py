import os,json
from django.conf import settings

def run_static_analysis(upload_file_obj):

    IDA_ROOT = os.path.join(settings.PROJECT_DIR,'opseq_ida')
    ANN_ROOT = os.path.join(settings.PROJECT_DIR, 'ann_by_static')

    upload_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)

    ops_folder_path = os.path.join(IDA_ROOT,'ops')
    ops_file_path = os.path.join(ops_folder_path,os.path.splitext(upload_file_obj.upload_file.name)[0]+'.ops')
    fh_folder_path = os.path.join(IDA_ROOT,'fh')
    fh_file_path = os.path.join(fh_folder_path,os.path.splitext(upload_file_obj.upload_file.name)[0]+'.fh')
    static_analysis_json_path = os.path.join(os.path.join(ANN_ROOT,'test_result'),os.path.splitext(upload_file_obj.upload_file.name)[0]+'.json')

    cmd_run_ida_ops = 'python ' + IDA_ROOT + os.sep + 'make_idb_ops.py ' + upload_file_path
    cmd_run_ida_fh = 'python ' + IDA_ROOT + os.sep + 'make_fh.py ' + ops_file_path
    os.system(cmd_run_ida_ops)
    os.system(cmd_run_ida_fh)

    cmd_run_ann = 'python ' + ANN_ROOT + os.sep + 'ann_by_static.py -t ' + fh_file_path
    os.system(cmd_run_ann)

    static_analysis_json = open(static_analysis_json_path)
    ret_data = json.load(static_analysis_json)
    return ret_data