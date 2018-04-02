from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from .models import UploadFile, UploadFileMeta
from .forms import UploadForm, ReportForm
from .es_view import *
from .ida_make_ops import make_ops
import hashlib, sys,os, ssdeep, json


# Create your views here.

def upload(request):
    if request.method == "GET":
        upload_form = UploadForm()

    elif request.method == "POST":
        up_file = request.FILES['upload_file']
        up_file_md5 = get_hash_str(up_file)
        UploadFile_obj = UploadFile(id=up_file_md5,upload_file=up_file)
        UploadFile_obj.save()
        up_file_url = os.path.join(settings.MEDIA_ROOT,UploadFile_obj.upload_file.name)
        #ops_file_url = make_ops(up_file_url)
        #sys.stderr.write(up_file_url)
        up_file_ssdeep = ssdeep.hash_from_file(up_file_url)
        #'sys.stderr.write(up_file_ssdeep)
        UploadFileMeta_obj = UploadFileMeta(id=up_file_md5,ssdeep=up_file_ssdeep)
        UploadFileMeta_obj.save()
        
        response = {'status':200,'pk':up_file_md5}
        return HttpResponse(json.dumps(response), content_type='application/json')
		
    ctx = {'upload_form': upload_form,}

    return render(request, 'upload.html',  ctx)


def detail(request, md5):
    if request.method == "GET":
        md5_form = ReportForm()
        ssdeep_forms = list()
        ctx = {'md5_form': md5_form, 'ssdeep_forms' : ssdeep_forms}

        try:
            UploadFileMeta_obj = UploadFileMeta.objects.get(pk=md5)
        except:
            return HttpResponse("Abnormal approach")

        es_md5_report = es_md5_search(UploadFileMeta_obj.pk)
        if es_md5_report is not 0:
            md5_form = create_report_form(md5_form,es_md5_report)
            ctx['md5_form'] = md5_form
        else:
            ctx['md5_form'] = 0

        es_ssdeep_report = es_ssdeep_search(UploadFileMeta_obj.ssdeep)
        if es_ssdeep_report is not 0:
            for idx in range(len(es_ssdeep_report)):
                ssdeep_form = ReportForm()
                ssdeep_form = create_report_form(ssdeep_form,es_ssdeep_report[idx])
                ssdeep_forms.append(ssdeep_form)

            ctx['ssdeep_forms'] = ssdeep_forms
        else:
            ctx['ssdeep_forms'] = 0

    #sys.stderr.;ft1'459/2cfhimruw3-write(str(es_ssdeep_report))

    return render(request, 'detail.html', ctx)


def create_report_form(report_form, es_report):
    report_form.fields['md5'].initial = es_report['_id']
    report_form.fields['file_size'].initial = int(es_report['_source']['File_Size'])
    report_form.fields['magic'].initial = es_report['_source']['Magic']
    report_form.fields['sha1'].initial = es_report['_source']['SHA-1']
    report_form.fields['sha256'].initial = es_report['_source']['SHA-256']
    report_form.fields['ssdeep'].initial = es_report['_source']['SSDeep']
    report_form.fields['detected'].initial = es_report['_source']['detected']
    report_form.fields['result'].initial = es_report['_source']['result']
    report_form.fields['uploaded_date'].initial = es_report['_source']['Uploaded_Date']
    report_form.fields['score'].initial = int(es_report['_score'])

    return report_form


def get_hash_str(upload_file, block_size = 8192 ) :
    md5 = hashlib.md5()
    f = upload_file
    while True :
        buf = f.read(block_size)
        if not buf :
            break
        md5.update(buf)
    return md5.hexdigest()

