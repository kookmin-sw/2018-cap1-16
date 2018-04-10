from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import UploadFile
from .forms import UploadForm, ReportForm
#from .ida.make_ops import make_ops
#from .ida.make_fh import make_fh
from .mongodb.md5_search import md5_search
from .es.es_view import es_ssdeep_search
import hashlib, sys,os, json

test_md5 = 'fffde1818e6c06ee3a030065d3325e28'

def upload(request):
    if request.method == "GET":
        upload_form = UploadForm()

    elif request.method == "POST":
        analysis_type = request.POST.get('analysis_radio')
        if(analysis_type == 'static'):
            analysis_type = 0
        elif(analysis_type == 'dynamic'):
            analysis_type = 1
        elif(analysis_type == 'hybrid'):
            analysis_type = 2

        upload_file = request.FILES['upload_file']
        upload_file_md5 = get_hash_str(upload_file)

        UploadFile_obj = UploadFile(id=test_md5,upload_file=upload_file,analysis_type=analysis_type)
        UploadFile_obj.save()

        #response = {'status':200,'pk':up_file_md5}
        response = {'status': 200, 'pk': test_md5}
        return HttpResponse(json.dumps(response), content_type='application/json')
		
    ctx = {'upload_form': upload_form,}

    return render(request, 'upload.html',  ctx)


def detail(request, md5):
    if request.method == "GET":
        try:
            upload_file_obj = UploadFile.objects.get(pk=md5)
        except:
            return HttpResponse("Abnormal approach")

        report_form = ReportForm()
        similar_report_forms = list()
        ctx = {'report_form': report_form, 'similar_report_forms' : similar_report_forms}

        analysis_type = upload_file_obj.analysis_type

        md5_search_data = md5_search(md5)
        if md5_search_data is not 0:
            md5_search_result_form = create_report_form(report_form,md5_search_data)
            ctx['report_form'] = md5_search_result_form
        else:
            if analysis_type == 0:
                #ops_path = get_ops_file_path(upload_file_obj)
                #fh_path = get_fh_file_path(upload_file_obj)
                ctx['report_form'] = 0

        #es_ssdeep_report = es_ssdeep_search(UploadFileMeta_obj.ssdeep)
        #if es_ssdeep_report is not 0:
        #    for idx in range(len(es_ssdeep_report)):
        #        ssdeep_form = ReportForm()
        #        ssdeep_form = create_report_form(ssdeep_form,es_ssdeep_report[idx])
        #        ssdeep_forms.append(ssdeep_form)

        #    ctx['ssdeep_forms'] = ssdeep_forms
        #else:
        #    ctx['ssdeep_forms'] = 0

    return render(request, 'detail.html', ctx)


def create_report_form(report_form, search_data):
    report_form.fields['md5'].initial = search_data['_id']
    report_form.fields['file_size'].initial = int(search_data['file_size'])
    report_form.fields['sha1'].initial = search_data['SHA-1']
    report_form.fields['sha256'].initial = search_data['SHA-256']
    #report_form.fields['ssdeep'].initial = search_data['SSDeep']
    report_form.fields['detected'].initial = search_data['detected']
    report_form.fields['label'].initial = search_data['label']
    report_form.fields['uploaded_date'].initial = search_data['Uploaded_Date']
    #report_form.fields['score'].initial = int(search_data['_score'])

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

#def get_ops_file_path(upload_file_obj):
#    up_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)
#    ops_file_path = make_ops(up_file_path)
#    return ops_file_path

#def get_fh_file_path(upload_file_obj):
#    up_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)
#    fh_file_path = make_fh(up_file_path)
#    return fh_file_path
