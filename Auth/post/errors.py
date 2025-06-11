from django.shortcuts import render

def custom_permission_denied_view(request, exeption=None):
    return render(request, '403.html', status=403)

def custom_page_not_found_view(request, exeption=None):
    return render(request, '404.html', status=404)