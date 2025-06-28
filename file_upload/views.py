from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .models import FileUpload, CreateFolder
from .forms import FileForm , FolderForm
import mimetypes
import os

# Create your views here.

#--------------file based views--------------
class CreateFile(CreateView):
    form_class = FileForm
    template_name = 'file_upload/create_file.html'
    
    def get_success_url(self):
        folder_id = self.kwargs.get('folder_id')
        if folder_id:
            return reverse_lazy('file_upload:folder_files', kwargs={'folder_id': folder_id})
        return reverse_lazy('file_upload:list_file')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pre-populate the folder field if we're creating a file within a folder
        folder_id = self.kwargs.get('folder_id')
        if folder_id and not kwargs.get('data'):
            try:
                parent_folder = CreateFolder.objects.get(id=folder_id)
                kwargs['initial'] = {'folder': parent_folder}
            except CreateFolder.DoesNotExist:
                pass
        return kwargs
    
    def form_valid(self, form):
        try:
            file_instance = form.save(commit=False)
            file_instance.uploaded_by = self.request.user
            file_instance.save()
            messages.success(self.request, f'File "{file_instance.name}" uploaded successfully!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error uploading file: {str(e)}')
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder_id = self.kwargs.get('folder_id')
        if folder_id:
            try:
                current_folder = CreateFolder.objects.get(id=folder_id)
                context['current_folder'] = current_folder
                context['parent_folder'] = current_folder
            except CreateFolder.DoesNotExist:
                pass
        return context

class ListFile(ListView):
    template_name = 'file_upload/list_file.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        folder_id = self.kwargs.get('folder_id')
        if folder_id:
            return FileUpload.objects.filter(folder_id=folder_id)
        else:
            return FileUpload.objects.filter(folder__isnull=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder_id = self.kwargs.get('folder_id')
        if folder_id:
            folders = CreateFolder.objects.filter(parent_id=folder_id)
            current_folder = get_object_or_404(CreateFolder, id=folder_id)
            context['current_folder'] = current_folder
            breadcrumbs = []
            parent = current_folder.parent
            while parent:
                breadcrumbs.insert(0, parent)
                parent = parent.parent
            context['breadcrumbs'] = breadcrumbs
        else:
            folders = CreateFolder.objects.filter(parent__isnull=True)
            context['current_folder'] = None
            context['breadcrumbs'] = []
        
        context['folders'] = folders
        context['total_items'] = context['object_list'].count() + folders.count()
        return context

class DetailFile(DetailView):
    template_name = 'file_upload/detail_file.html'
    context_object_name = 'file'

    def get_object(self):
        file_id = self.kwargs.get('id')
        file = get_object_or_404(FileUpload, id=file_id)
        file_url = file.file.url
        file_path = file.file.path

        file.mime_type = mimetypes.guess_type(file_path)[0]
        return file

class DeleteFile(DeleteView):
    model = FileUpload
    template_name = 'file_upload/delete_file.html'
    success_url = reverse_lazy('file_upload:list_file')
    context_object_name = 'file'
    
    def get_object(self):
        file_id = self.kwargs.get('id')
        return get_object_or_404(FileUpload, id=file_id)
    
    def delete(self, request, *args, **kwargs):
        file = self.get_object()
        messages.success(request, f'File "{file.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)

#---------------- file based views end --------------


#---------------- folder based views--------------
class CreateFolderView(CreateView):
    form_class = FolderForm
    template_name = 'file_upload/create_folder.html'
    
    def get_success_url(self):
        # Redirect back to the current folder if we're in one, otherwise to root
        folder_id = self.kwargs.get('folder_id')
        if folder_id:
            return reverse_lazy('file_upload:folder_files', kwargs={'folder_id': folder_id})
        return reverse_lazy('file_upload:list_file')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pre-populate the parent field if we're creating a folder within another folder
        folder_id = self.kwargs.get('folder_id')
        if folder_id and not kwargs.get('data'):
            try:
                parent_folder = CreateFolder.objects.get(id=folder_id)
                kwargs['initial'] = {'parent': parent_folder}
            except CreateFolder.DoesNotExist:
                pass
        return kwargs
    
    def form_valid(self, form):
        try:
            folder = form.save()
            messages.success(self.request, f'Folder "{folder.name}" created successfully!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error creating folder: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder_id = self.kwargs.get('folder_id')
        if folder_id:
            try:
                current_folder = CreateFolder.objects.get(id=folder_id)
                context['current_folder'] = current_folder
                context['parent_folder'] = current_folder
            except CreateFolder.DoesNotExist:
                pass
        context['folders'] = CreateFolder.objects.all()
        return context

class ListFolder(ListView):
    template_name = 'file_upload/list_folder.html'
    context_object_name = 'folders'
    queryset = CreateFolder.objects.all()

class DetailFolder(DetailView):
    template_name = 'file_upload/detail_folder.html'
    context_object_name = 'folder'

    def get_object(self):
        folder_id = self.kwargs.get('id')
        return get_object_or_404(CreateFolder, id=folder_id)

class DeleteFolder(DeleteView):
    model = CreateFolder
    template_name = 'file_upload/delete_folder.html'
    success_url = reverse_lazy('file_upload:list_file')
    context_object_name = 'folder'
    
    def get_object(self):
        folder_id = self.kwargs.get('id')
        return get_object_or_404(CreateFolder, id=folder_id)
    
    def delete(self, request, *args, **kwargs):
        folder = self.get_object()
        messages.success(request, f'Folder "{folder.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
#---------------- folder based views end --------------