from .forms import *

def create_static_report_form(search_data):
    report_form = ReportForm()
    report_form.fields['md5'].initial = search_data['md5']
    report_form.fields['detected'].initial = search_data['detected']
    report_form.fields['label'].initial = search_data['label']
    report_form.fields['collected_date'].initial = search_data['collected_date']
    #report_form.fields['score'].initial = int(search_data['score'])
    report_form.fields['score'].initial = 100
    return report_form

def create_dynamic_report_form(search_data):
    report_form = ReportForm()
    report_form.fields['md5'].initial = search_data['target']['file']['md5']

    signature_forms = list()
    try:
        for idx in range(len(search_data['signatures'])):
            signature_form = SignatureForm()
            signature_form.fields['description'].initial = search_data['signatures'][idx]['description']
            signature_form.fields['severity'].initial = search_data['signatures'][idx]['severity']
            signature_forms.append(signature_form)
    except:
        signature_forms = None

    DLL_forms = list()
    try:
        for idx in range(len(search_data['summary']['dll_loaded'])):
            DLL_form = DLLForm()
            DLL_form.fields['DLL_name'].initial = search_data['summary']['dll_loaded'][idx]
            DLL_forms.append(DLL_form)
    except:
        DLL_forms = None

    connects_host_forms = list()
    try:
        for idx in range(len(search_data['summary']['connects_host'])):
            connects_host_form = ConnectsHostForm()
            connects_host_form.fields['host'].initial = search_data['summary']['connects_host'][idx]
            connects_host_forms.append(connects_host_form)
    except:
        connects_host_forms = None

    connects_ip_forms = list()
    try:
        for idx in range(len(search_data['summary']['connects_ip'])):
            connects_ip_form = ConnectsIpForm()
            connects_ip_form.fields['host'].initial = search_data['summary']['connects_ip'][idx]
            connects_ip_forms.append(connects_ip_form)
    except:
        connects_ip_forms = None

    return report_form, signature_forms, DLL_forms, connects_host_forms, connects_ip_forms

def create_classfication_data_form(detected, result_bc, result_mc):
    classificationData = ClassificationDataForm()
    classificationData.fields['detected'].initial = detected
    classificationData.fields['result_bc'].initial = result_bc
    classificationData.fields['result_mc'].initial = result_mc
    return classificationData


