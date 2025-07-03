from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('file_upload:list_file')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('file_upload:list_file')
    return wrapper_func