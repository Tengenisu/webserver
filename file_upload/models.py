from django.db import models
from django.contrib.auth.models import User
import os
class CreateFolder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self' , null=True , blank=True, on_delete=models.CASCADE , related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# Create your models here.
class FileUpload(models.Model):
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=20 , blank=False)
    folder = models.ForeignKey(CreateFolder , on_delete=models.CASCADE, null=True , blank=True)
    file = models.FileField(upload_to='uploads/files')
    uploaded_by = models.ForeignKey(User , on_delete=models.CASCADE , null=True, related_name='uploaded_files' )
    deleted_by = models.ForeignKey(User , on_delete=models.CASCADE , null=True , blank=True,related_name='deleted_files')

    def save(self, *args , **kwargs): #run when we create a new file
        if not self.file.name:
            raise ValueError("File is required")
        file_path = str(self.file.name)
        file_root , file_ext = os.path.splitext(file_path)
        if not self.name:
            self.name = file_root
        if not self.extension:
            self.extension = file_ext.lstrip('.').lower() #removes the . and converts to lowercase example hello.PDF -> pdf
        super().save(*args , **kwargs)

    def __str__(self):
        return self.name