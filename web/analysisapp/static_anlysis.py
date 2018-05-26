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

    # packer_info
    packer_report = dict()
    packer_info = peviewer.get_packer_info()
    if not len(packer_info) == 0:
        for i, packer in enumerate(packer_info):
            packer_report[str(i)] = packer
        total_report['packer_info'] = packer_report
    else:
        total_report['packer_info'] = 'None'

    # section_number
    section_num = peviewer.get_section_number()
    total_report['section_num'] = section_num

    # section_nfo
    section_report = dict()
    section_info = peviewer.get_sections_info()
    if not len(section_info) == 0:
        for i, section in enumerate(section_info):
            section_report[str(i)] = section
        total_report['section_info'] = section_report
    else:
        total_report['section_info'] = 'None'

    # compile_time
    total_report['compile_time'] = peviewer.get_compile_time()

    # resource_info
    resource_report = dict()
    resource_info = peviewer.get_resources_info()
    if not len(resource_info) == 0:
        for i, resource in enumerate(resource_info):
            resource_report[str(i)] = resource
        total_report['resource_info'] = resource_report
    else:
        total_report['resource_info'] = 'None'

    # import_function
    import_func_report = dict()
    import_func_info = peviewer.get_import_function()
    if not len(import_func_info) == 0:
        for i, import_func in enumerate(import_func_info):
            import_func_report[str(i)]=import_func.decode('ascii')
        total_report['import_function'] = import_func_report
    else:
        total_report['import_function'] = "None"

    # mutex_info
    mutex_report = dict()
    mutex_info = peviewer.get_mutex_info()
    if not len(mutex_info) == 0:
        for i, mutex in enumerate(mutex_info):
            mutex_report[str(i)]=mutex
        total_report['mutex_info'] = mutex_report
    else:
        total_report['mutex_info'] = "None"

    # api_alert_info
    api_alert_report = dict()
    api_alert_info = peviewer.get_api_alert_info()
    if not len(api_alert_info) == 0:
        for i, api_alert in enumerate(api_alert_info):
            api_alert_report[str(i)] = api_alert
        total_report['api_alert_info'] = api_alert_report
    else:
        total_report['api_alert_info'] = 'None'

    return total_report