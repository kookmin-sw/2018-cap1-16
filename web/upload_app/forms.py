from django import forms
from .models import UploadFile

class UploadForm(forms.ModelForm):
	class Meta:
		model = UploadFile
		fields = ('upload_file',)

class ReportForm(forms.Form): 
    md5 = forms.CharField(max_length=255)
    file_size = forms.IntegerField()
    sha1 = forms.CharField(max_length=255)
    sha256 = forms.CharField(max_length=255)
    ssdeep = forms.CharField(max_length=255)
    detected = forms.CharField(max_length=255)
    label = forms.CharField(max_length=255)
    score = forms.CharField(max_length=255)
    collected_date = forms.DateTimeField()

