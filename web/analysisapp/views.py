from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from .models import UploadFile
from .forms import *
from .md5 import get_hash_str
from .es.es_search import *
from .es.upload import *
from .static_anlysis import *
from .dynamic_anlysis import *
from .create_form import *
import sys,os, json,time


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

        md5_search_data = es_static_testing_result_search(file_md5)
        if md5_search_data is not None:
            ctx['status'] = 200
        else:
            result_bc, result_mc = run_static_testing(upload_file_obj)
            #es_upload_static_testing_result(md5,result_bc,result_mc)
            result_peviewer = run_pefile_viewer(upload_file_obj)
            es_upload_peviewer_result(md5,result_peviewer)
            time.sleep(0.5)
            ctx['status'] = 200

        return HttpResponse(ctx)

def dynamic_analysis(request,md5):
    dy_test_md5 = 'a1f1c980d0bdc805633f2340eecdcb93'
    if request.method == "GET":
        ctx = {'file_md5': dy_test_md5}
        return render(request,'loading_dynamic_analysis.html',ctx)

    elif request.method == "POST":
        file_md5 = md5
        #try:
        #    upload_file_obj = UploadFile.objects.get(pk=file_md5)
        #except:
        #    return HttpResponse("Abnormal approach")

        ctx = {'status': 500}

        md5_search_data = es_dynamic_report_search(dy_test_md5)
        if md5_search_data is not None:
            ctx['status'] = 200
        else:
            run_dynamic_analysis(upload_file_obj)
            ctx['status'] = 200

        result_bc, result_mc = run_dynamic_clasification(dy_test_md5)
        es_upload_dynamic_testing_result(dy_test_md5,result_bc,result_mc)
        time.sleep(0.5)

        return HttpResponse(ctx)

def static_report_view(request, md5):
    if request.method == "GET":
        ctx = {'report_form': None, 'classification_data_form':None, 'similar_report_forms' : None}

        # Let's search from elasticsearch
        static_testing_result_data = es_static_testing_result_search(md5)

        # Create report form
        if static_testing_result_data is not None:
            static_report_form, classfication_data_form = create_static_report_form(static_testing_result_data)
            ctx['report_form'] = static_report_form
            ctx['classification_data_form'] = classfication_data_form
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

        ctx = {'report_form': None,'classification_data_form':None , 'signature_forms':None, 'DLL_forms': None, 'connects_host_forms': None, 'connects_ip_forms': None}

        # Let's search from elasticsearch
        cuckoo_search_data = es_dynamic_report_search(md5)
        dynamic_testing_result_data = es_dynamic_testing_result_search(md5)

        # Create report form
        if cuckoo_search_data is not None:
            dynamic_report_form, classification_data_form, signature_forms, DLL_forms, connects_host_forms, connects_ip_forms= create_dynamic_report_form(cuckoo_search_data, dynamic_testing_result_data)

            ctx['report_form'] = dynamic_report_form
            ctx['classification_data_form'] = classification_data_form
            ctx['signature_forms'] = signature_forms
            ctx['DLL_forms'] = DLL_forms
            ctx['connects_host_forms'] = connects_host_forms
            ctx['connects_ip_forms'] = connects_ip_forms
        else:
            return HttpResponse("Abnormal approach")

    return render(request, 'dynamic_report.html',ctx)
