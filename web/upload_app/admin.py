from django.contrib import admin
from .models import ReportFile, UploadFile, UploadFileMeta
# Register your models here.

admin.site.register(ReportFile)
admin.site.register(UploadFile)
admin.site.register(UploadFileMeta)
