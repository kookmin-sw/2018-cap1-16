from .forms import *

def create_static_report_form(search_data):
    report_form = ReportForm()
    report_form.fields['md5'].initial = search_data['md5']
    report_form.fields['collected_date'].initial = search_data['collected_date']
    classfication_data_form = create_classfication_data_form(search_data['detected'],search_data['result_bc'],search_data['result_mc'])
    return report_form, classfication_data_form

def create_peviewer_section_forms(search_data):

    peviewer_report_forms = list()

    try:
        section_info = search_data['section_info']
    except:
        section_info = None

    if not section_info == None:
        for section in section_info:
            peviewer_section_form = PeviewerSectionInfoForm()
            peviewer_section_form.fields['name'].initial = section['name']
            peviewer_section_form.fields['hash_md5'].initial = section['hash_md5']
            peviewer_section_form.fields['hash_sha1'].initial = section['hash_sha1']
            peviewer_section_form.fields['suspicious'].initial = section['suspicious']
            peviewer_section_form.fields['virtual_address'].initial = section['virtual_address']
            peviewer_section_form.fields['virtual_size'].initial = section['virtual_size']
            peviewer_section_form.fields['size_raw_data'].initial = section['size_raw_data']
            peviewer_report_forms.append(peviewer_section_form)
    else:
        peviewer_report_forms = None

    return peviewer_report_forms

def create_peviewer_import_function_forms(search_data):

    peviewer_import_function_forms = list()

    try:
        import_functions = search_data['import_function']
    except:
        import_functions= None

    if not import_functions == None:
        for import_function in import_functions:
            peviewer_import_function_form = PeviewerImportFunctionForm()
            peviewer_import_function_form.fields['name'].initial = import_function
            peviewer_import_function_forms.append(peviewer_import_function_form)
    else:
        peviewer_import_function_forms = None

    return peviewer_import_function_forms

def create_peviewer_packer_info_forms(search_data):

    peviewer_packer_info_forms = list()
    try:
        packer_infos = search_data['packer_info']
    except:
        packer_infos= None

    if not packer_infos == None:
        for packer_info in packer_infos:
            peviewer_packer_info_form = PeviewerPackerInfoForm()
            peviewer_packer_info_form.fields['name'].initial = packer_info
            peviewer_packer_info_forms.append(peviewer_packer_info_form)
    else:
        peviewer_packer_info_forms = None

    return peviewer_packer_info_forms

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


