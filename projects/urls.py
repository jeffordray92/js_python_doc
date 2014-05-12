from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jumpstart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'projects.views.project_list', name="projects"),
    url(r'^edit/(?P<id>\d+)/(?P<slug>[-_\w]+)/$', 'projects.views.edit', name='project_edit'),
    url(r'^details/(?P<id>\d+)/(?P<slug>[-_\w]+)/$', 'projects.views.details', name='project_details'),
    url(r'^details/(?P<id>\d+)/(?P<slug>[-_\w]+)/(?P<setup_type>[-_\w]+)/(?P<success>[-_\w]+)/$', 'projects.views.details', name='project_details'),
    url(r'^add/$', 'projects.views.add', name='project_add'),
)