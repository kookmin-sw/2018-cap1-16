from .forms import *

def create_static_report_form(search_data):
    report_form = ReportForm()
    report_form.fields['md5'].initial = search_data['md5']
    report_form.fields['collected_date'].initial = search_data['collected_date']
    classfication_data_form = create_classfication_data_form(search_data['detected'],search_data['result_bc'],search_data['result_mc'])
    return report_form, classfication_data_form

def create_peviewer_section_form(search_data):
    section_info = search_data['section_info']

    peviewer_report_form = ReportForm()
    return peviewer_report_form

def create_dynamic_report_form(search_data,testing_search_data):
    print(testing_search_data)
    report_form = ReportForm()
    report_form.fields['md5'].initial = search_data['target']['file']['md5']
    report_form.fields['collected_date'].initial = testing_search_data['collected_date']

    # signatures info
    signature_forms = list()
    try:
        for idx in range(len(search_data['signatures'])):
            signature_form = SignatureForm()
            signature_form.fields['description'].initial = search_data['signatures'][idx]['description']
            signature_form.fields['severity'].initial = search_data['signatures'][idx]['severity']
            signature_forms.append(signature_form)
    except:
        signature_forms = None

    # ai classification
    classification_data_form = create_classfication_data_form(testing_search_data['detected'],testing_search_data['result_bc'],testing_search_data['result_mc'])

    # import dll
    DLL_forms = list()
    try:
        for idx in range(len(search_data['summary']['dll_loaded'])):
            DLL_form = DLLForm()
            DLL_form.fields['DLL_name'].initial = search_data['summary']['dll_loaded'][idx]
            DLL_forms.append(DLL_form)
    except:
        DLL_forms = None

    # connects host info
    connects_host_forms = list()
    try:
        for idx in range(len(search_data['summary']['connects_host'])):
            connects_host_form = ConnectsHostForm()
            connects_host_form.fields['host'].initial = search_data['summary']['connects_host'][idx]
            connects_host_forms.append(connects_host_form)
    except:
        connects_host_forms = None

    # connects ip info
    connects_ip_forms = list()
    try:
        for idx in range(len(search_data['summary']['connects_ip'])):
            connects_ip_form = ConnectsIpForm()
            connects_ip_form.fields['host'].initial = search_data['summary']['connects_ip'][idx]
            connects_ip_forms.append(connects_ip_form)
    except:
        connects_ip_forms = None

    return report_form, classification_data_form, signature_forms, DLL_forms, connects_host_forms, connects_ip_forms

def create_classfication_data_form(detected, result_bc, result_mc):
    classificationData = ClassificationDataForm()
    classificationData.fields['detected'].initial = detected
    classificationData.fields['result_bc'].initial = result_bc
    classificationData.fields['result_mc'].initial = result_mc
    return classificationData


