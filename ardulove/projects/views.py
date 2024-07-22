from django.shortcuts import render, get_object_or_404

from .models import Project, ProjectTag


def project_main(request):
    tag_id = request.GET.get('tag')
    if tag_id:
        projects = Project.objects.filter(tags__id=tag_id).order_by('-id')
    else:
        projects = Project.objects.all().order_by('-id')

    tags = ProjectTag.objects.all()
    return render(request, 'projects/projects.html', {'projects': projects, 'tags': tags})


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})
