# Generated by Django 5.2.3 on 2025-06-28 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0004_rename_folder_createfolder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file_upload.createfolder'),
        ),
    ]
