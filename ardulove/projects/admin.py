from django.contrib import admin
from .models import Project, ProjectTag


class ProjectAdmin(admin.ModelAdmin):
    pass


class ProjectTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTag, ProjectTagAdmin)
