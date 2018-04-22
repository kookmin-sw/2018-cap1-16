import os,sys
from django.conf import settings

CUCKOO_ROOT = os.path.join(settings.PROJECT_DIR,'cuckoo')
CUCKOO_SCRIPT_ROOT = os.path.join(CUCKOO_ROOT,'scripts')
sys.path.append(CUCKOO_SCRIPT_ROOT)
import upload_file

def run_dynamic_analysis(upload_file_obj):

    upload_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)

    #cmd_run_cuckoo_upload = 'python ' + CUCKOO_SCRIPT_ROOT + os.sep + 'upload_file.py ' + upload_file_path
    #os.system(cmd_run_cuckoo_upload)
    dynamic_analysis_data = upload_file.run(upload_file_path)
    print(dynamic_analysis_data)
    return dynamic_analysis_data