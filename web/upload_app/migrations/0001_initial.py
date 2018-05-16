# Generated by Django 2.0.4 on 2018-04-16 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportFile',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('file_size', models.IntegerField()),
                ('magic', models.CharField(max_length=255)),
                ('sha1', models.CharField(max_length=255)),
                ('sha256', models.CharField(max_length=255)),
                ('ssdeep', models.CharField(max_length=255)),
                ('detected', models.CharField(max_length=255)),
                ('result', models.CharField(max_length=255)),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('upload_file', models.FileField(upload_to='')),
                ('analysis_type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFileMeta',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('ssdeep', models.CharField(max_length=255)),
            ],
        ),
    ]
