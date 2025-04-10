from django.shortcuts import render
from projects.models import Project


def index(request):
    projects = Project.objects.all().order_by('-id')[:10]
    return render(request, 'index.html', {'projects': projects})


def contact_page(request):
    return render(request, 'contact.html')
