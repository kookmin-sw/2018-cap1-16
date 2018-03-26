from django import forms
from .models import UploadFile

class UploadForm(forms.ModelForm):
	class Meta:
		model = UploadFile
		fields = ('upload_file',)

class ReportForm(forms.Form): 
    md5 = forms.CharField(max_length=255)
    file_size = forms.IntegerField()
    magic = forms.CharField(max_length=255)
    sha1 = forms.CharField(max_length=255)
    sha256 = forms.CharField(max_length=255)
    ssdeep = forms.CharField(max_length=255)
    detected = forms.CharField(max_length=255)
    result = forms.CharField(max_length=255)
    score = forms.CharField(max_length=255)
    uploaded_date = forms.DateTimeField()

