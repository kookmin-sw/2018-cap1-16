from .forms import UploadForm, ReportForm, SignatureForm

def create_static_report_form(report_form, search_data):
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
    for idx in range(len(search_data['signatures'])):
        signature_form = SignatureForm()
        signature_form.fields['description'].initial = search_data['signatures'][idx]['description']
        signature_form.fields['severity'].initial = search_data['signatures'][idx]['severity']
        signature_forms.append(signature_form)

    return report_form, signature_forms