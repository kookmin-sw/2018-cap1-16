# Generated by Django 2.0.3 on 2018-04-28 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysisapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfile',
            name='analysis_type',
        ),
    ]