from django.shortcuts import render
from django.http import HttpResponse
from .md5 import get_hash_str
from mask_elasticsearch.search import *
from mask_elasticsearch.upload import *
from .static_anlysis import *
from .dynamic_anlysis import *
from .create_form import *
import json,time, ssdeep

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
        upload_file_buf = upload_file.read()

        pe_signal = str(upload_file_buf[:2].decode())
        if not pe_signal == 'MZ':
            response = {'status': 406, 'message': 'Does not support Not PE File'}
            return HttpResponse(json.dumps(response), content_type='application/json')

        upload_file_md5 = get_hash_str(upload_file_buf)
        upload_file_ssdeep = ssdeep.hash(upload_file_buf)

        UploadFile_obj = UploadFile(id=upload_file_md5,upload_file=upload_file,ssdeep=upload_file_ssdeep)
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
            es_upload_static_testing_result(md5,result_bc,result_mc)

            result_peviewer = run_pefile_viewer(upload_file_obj)
            es_upload_peviewer_result(md5,result_peviewer)

            time.sleep(0.5)
            ctx['status'] = 200

        return HttpResponse(ctx)

def dynamic_analysis(request,md5):
    dy_test_md5 = '0068ca1fd8423275ba33daa962421c2f'
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

        result_bc, result_mc = run_dynamic_clasification(file_md5)
        es_upload_dynamic_testing_result(file_md5,result_bc,result_mc)
        time.sleep(0.5)

        return HttpResponse(ctx)

def static_report_view(request, md5):
    if request.method == "GET":
        ctx = {'basic_report_form': None,
               'classification_data_form':None,
               'peviewer_basic_info_form': None,
               'peviewer_packer_info_forms':None,
               'peviewer_section_forms': None,
               'peviewer_import_function_forms': None,
               'peviewer_api_alert_info_forms' : None,
               'similar_file_forms' : None}

        upload_file_ssdeep = UploadFile.objects.get(pk=md5).ssdeep

        # Let's search from mask_elasticsearch
        static_testing_result_data = es_static_testing_result_search(md5)
        peviewer_search_data = es_search_peviewer_result(md5)
        similar_file_search_data = es_search_similar_file(upload_file_ssdeep)

        # Create report form
        if static_testing_result_data is not None:
            basic_report_form = create_static_report_form(static_testing_result_data)
            classfication_data_form = create_classfication_data_form(static_testing_result_data)
            peviewer_basic_info_form = create_peviewer_basic_info_form(peviewer_search_data)
            peviewer_packer_info_forms = create_peviewer_packer_info_forms(peviewer_search_data)
            peviewer_section_forms = create_peviewer_section_forms(peviewer_search_data)
            peviewer_import_function_forms = create_peviewer_import_function_forms(peviewer_search_data)
            peviewer_api_alert_info_forms = create_api_alert_info_forms(peviewer_search_data)
            similar_file_forms = create_similar_file_form(similar_file_search_data)

            ctx['basic_report_form'] = basic_report_form
            ctx['peviewer_basic_info_form'] = peviewer_basic_info_form
            ctx['peviewer_packer_info_forms'] = peviewer_packer_info_forms
            ctx['peviewer_section_forms'] = peviewer_section_forms
            ctx['peviewer_import_function_forms'] = peviewer_import_function_forms
            ctx['peviewer_api_alert_info_forms'] = peviewer_api_alert_info_forms
            ctx['classification_data_form'] = classfication_data_form
            ctx['similar_file_forms'] =similar_file_forms
        else:
            return HttpResponse("Abnormal approach")

    return render(request, 'static_report.html',ctx)

def dynamic_report_view(request, md5):
    if request.method == "GET":

        ctx = {'basic_report_form': None,'classification_data_form':None , 'signature_forms':None, 'DLL_forms': None, 'connects_host_forms': None, 'connects_ip_forms': None}

        # Let's search from mask_elasticsearch
        cuckoo_search_data = es_dynamic_report_search(md5)
        dynamic_testing_result_data = es_dynamic_testing_result_search(md5)

        # Create report form
        if cuckoo_search_data is not None:
            basic_report_form, signature_forms, DLL_forms, connects_host_forms, connects_ip_forms= create_dynamic_report_form(cuckoo_search_data)
            classification_data_form = create_classfication_data_form(dynamic_testing_result_data)

            ctx['basic_report_form'] = basic_report_form
            ctx['classification_data_form'] = classification_data_form
            ctx['signature_forms'] = signature_forms
            ctx['DLL_forms'] = DLL_forms
            ctx['connects_host_forms'] = connects_host_forms
            ctx['connects_ip_forms'] = connects_ip_forms
        else:
            return HttpResponse("Abnormal approach")

    return render(request, 'dynamic_report.html',ctx)
