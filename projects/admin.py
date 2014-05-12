from django.contrib import admin

from projects.models import (
    Project, 
    ProjectManagement, 
    ProjectRepository, 
    ProjectTemplate,
    ProjectTestSite,
    ProjectType,
)

admin.site.register(Project)
admin.site.register(ProjectType)
admin.site.register(ProjectTemplate)
admin.site.register(ProjectRepository)
admin.site.register(ProjectManagement)
admin.site.register(ProjectTestSite)