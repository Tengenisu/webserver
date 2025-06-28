from django.contrib import admin
from django.urls import path
from .views import CreateFile, ListFile, DetailFile, DeleteFile, CreateFolderView, ListFolder, DetailFolder, DeleteFolder

app_name='file_upload'
urlpatterns = [
    path('create_file/', CreateFile.as_view(), name='create_file'),
    path('list_file/', ListFile.as_view(), name='list_file'),
    path('detail_file/<int:id>/', DetailFile.as_view(), name='detail_file'),
    path('delete_file/<int:id>/', DeleteFile.as_view(), name='delete_file'),
    path('create_folder/', CreateFolderView.as_view(), name='create_folder'),
    path('list_folder/', ListFolder.as_view(), name='list_folder'),
    path('detail_folder/<int:id>/', DetailFolder.as_view(), name='detail_folder'),
    path('delete_folder/<int:id>/', DeleteFolder.as_view(), name='delete_folder'),
    path('folder/<int:folder_id>/', ListFile.as_view(), name='folder_files'),
    path('folder/<int:folder_id>/create_folder/', CreateFolderView.as_view(), name='create_folder_in_folder'),
    path('folder/<int:folder_id>/create_file/', CreateFile.as_view(), name='create_file_in_folder'),
]
