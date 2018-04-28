from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from .models import UploadFile
from .forms import UploadForm, ReportForm
from .es.es_search import es_static_report_search
from .es.es_search import es_dynamic_report_search
from .static_anlysis import run_static_analysis
from .dynamic_anlysis import run_dynamic_analysis
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

        upload_file = request.FILES['upload_file']
        upload_file_md5 = get_hash_str(upload_file)

        UploadFile_obj = UploadFile(id=upload_file_md5,upload_file=upload_file)
        UploadFile_obj.save()

        response = {'status':200,'pk':upload_file_md5,'analysis_type':analysis_type}

        return HttpResponse(json.dumps(response), content_type='application/json')
		
    ctx = {'upload_form': upload_form,}

    return render(request, 'upload.html',  ctx)


def static_analysis(request,md5):

    if request.method == "GET":
        ctx = {'file_md5': md5}
        return render(request,'loading_static_analysis.html',ctx)

    elif request.method == "POST":
        file_md5 = md5
        try:
            upload_file_obj = UploadFile.objects.get(pk=file_md5)
        except:
            return HttpResponse("Abnormal approach")

        ctx = {'status': 500}

        md5_search_data = es_static_report_search(file_md5)
        if md5_search_data is not None:
            ctx['status'] = 200
        else:
            static_analysis_data = run_static_analysis(upload_file_obj)
            #upload_analysis_report(static_analysis_data)
            ctx['status'] = 200

        return HttpResponse(ctx)

def dynamic_analysis(request,md5):

    if request.method == "GET":
        ctx = {'file_md5': md5}
        return render(request,'loading_dynamic_analysis.html',ctx)

    elif request.method == "POST":
        file_md5 = md5
        try:
            upload_file_obj = UploadFile.objects.get(pk=file_md5)
        except:
            return HttpResponse("Abnormal approach")

        ctx = {'status': 500}

        md5_search_data = es_dynamic_report_search(file_md5)
        if md5_search_data is not None:
            ctx['status'] = 200
        else:
            run_dynamic_analysis(upload_file_obj)
            ctx['status'] = 200

        return HttpResponse(ctx)

def static_report_view(request, md5):
    if request.method == "GET":

        report_form = ReportForm()
        similar_report_forms = list()
        ctx = {'report_form': report_form, 'similar_report_forms' : similar_report_forms}

        # Let's search from elasticsearch
        md5_search_data = es_static_report_search(md5)


        # Create report form
        if md5_search_data is not None:
            md5_search_result_form = create_static_report_form(report_form,md5_search_data)
            ctx['report_form'] = md5_search_result_form
        else:
            return HttpResponse("Abnormal approach")

        #es_ssdeep_report = es_ssdeep_search(UploadFileMeta_obj.ssdeep)
        #if es_ssdeep_report is not 0:
        #    for idx in range(len(es_ssdeep_report)):
        #        ssdeep_form = ReportForm()
        #        ssdeep_form = create_report_form(ssdeep_form,es_ssdeep_report[idx])
        #        ssdeep_forms.append(ssdeep_form)

        #    ctx['ssdeep_forms'] = ssdeep_forms
        #else:
        #    ctx['ssdeep_forms'] = 0

    return render(request, 'static_report.html',ctx)

def dynamic_report_view(request, md5):
    if request.method == "GET":

        report_form = ReportForm()
        similar_report_forms = list()
        ctx = {'report_form': report_form, 'similar_report_forms' : similar_report_forms}

        # Let's search from elasticsearch
        md5_search_data = es_dynamic_report_search(md5)

        # Create report form
        if md5_search_data is not None:
            md5_search_result_form = create_dynamic_report_form(report_form,md5_search_data)
            ctx['report_form'] = md5_search_result_form
        else:
            return HttpResponse("Abnormal approach")

    return render(request, 'dynamic_report.html',ctx)

def create_static_report_form(report_form, search_data):
    report_form.fields['md5'].initial = search_data['md5']
    report_form.fields['detected'].initial = search_data['detected']
    report_form.fields['label'].initial = search_data['label']
    report_form.fields['collected_date'].initial = search_data['collected_date']
    #report_form.fields['score'].initial = int(search_data['score'])
    report_form.fields['score'].initial = 100
    return report_form

def create_dynamic_report_form(report_form,search_data):
    report_form.fields['md5'].initial = search_data['target']['file']['md5']

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



#def get_fh_file_path(upload_file_obj):
#    up_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)
#    fh_file_path = make_fh(up_file_path)
#    return fh_file_path
