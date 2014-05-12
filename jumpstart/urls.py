"""

The **jumpstart.urls.py*** is the main URL Configuration, which includes the general URL patterns

**URL Patterns:**
    * ``url(r'^$', 'jumpstart.views.home', name='home')``
        This redirects to the Home Page
    * ``url(r'^admin/', include(admin.site.urls))``
        for the admin site
    * ``url(r'^login/$', 'jumpstart.views.login', name="login")``
        Redirects to the Login view
    * ``url(r'^logout/$', 'jumpstart.views.logout', name="logout")``
        Redirects to the Logout view
    * ``url(r'^projects/', include("projects.urls"))``
        Links the URL patterns configured in the Projects module
    * ``url(r'^settings/', include("profiles.urls", namespace="profiles"))``
        Links the URL patterns configures in the Profiles module
    * ``url(r'^wiki/home', 'jumpstart.views.view_wiki', name = 'wiki')``
        Redirects to the Mezzanine-powered Wiki Home Page
    * ``url(r'^', include("mezzanine.urls"))``
        Links the URL patterns provided by Mezzanine

"""
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.utils.functional import curry
from django.views.defaults import *

from mezzanine.core.views import direct_to_template
#from jumpstart import settings


admin.autodiscover()

handler500 = curry(server_error, template_name='error500.html')
handler404 = curry(page_not_found, template_name='error404.html')
handler403 = curry(permission_denied, template_name='error403.html')
 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jumpstart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'jumpstart.views.home', name='home'),
    url(r'^login/$', 'jumpstart.views.login', name="login"),
    url(r'^logout/$', 'jumpstart.views.logout', name="logout"),
    url(r'^clone/$', 'jumpstart.utils.clone_template', name="clone_template"),
    url(r'^error/$', 'jumpstart.views.error', name="error"),
    url(r'^projects/', include("projects.urls")),
    url(r'^settings/', include("profiles.urls", namespace="profiles")),
    url(r'^wiki/home/$', 'jumpstart.views.wiki', name = 'wiki'),
    #url(r'^wiki/trial', 'mezzanine_utils.utils.get_path', name = 'get_path'),
    url(r'^', include("mezzanine.urls")),
    #url(r'^wiki/', direct_to_template, {"template": "index.html"}, name="wiki"),
)