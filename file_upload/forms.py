from django.forms import ModelForm
from .models import FileUpload, CreateFolder
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
import os

class FileForm(ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file', 'folder']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise ValidationError("Please select a file to upload.")
        
        # Check file size (limit to 50MB)
        if file.size > 50 * 1024 * 1024:
            raise ValidationError("File size must be less than 50MB.")
        
        # Check file extension
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.rar']
        file_extension = os.path.splitext(file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise ValidationError(f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}")
        
        return file

class FolderForm(ModelForm):
    class Meta:
        model = CreateFolder
        fields = ['name', 'parent']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check if name is provided
        if not name:
            raise ValidationError("Folder name is required.")
        
        # Check if name is not just whitespace
        if name.strip() == '':
            raise ValidationError("Folder name cannot be empty.")
        
        # Check for invalid characters
        INVALID_CHARS = r'[<>:"/\\|?*]'
        if re.search(INVALID_CHARS, name):
            raise ValidationError("Folder name contains invalid characters. Please avoid: < > : \" / \\ | ? *")
        
        # Check if folder name already exists in the same parent
        parent = self.cleaned_data.get('parent')
        existing_folders = CreateFolder.objects.filter(parent=parent, name__iexact=name)
        
        if self.instance.pk:
            existing_folders = existing_folders.exclude(pk=self.instance.pk)
        
        if existing_folders.exists():
            raise ValidationError("A folder with this name already exists in the same location.")
        
        return name.strip()