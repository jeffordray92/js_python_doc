"""

The **profiles.urls.py*** files involves URL patterns, attached to the URL pattern settings/

**URL Patterns:**
	* ``url(r'^$', 'settings', name='settings')``
		Redirects to the page where the user can view the current settings
	* ``url(r'^edit/(?P<pk>[-_\w]+)$', 'settings_edit', name='settings_edit')``
		Redirects to the page where the user can update the current settings

"""
from django.conf.urls import patterns, include, url


urlpatterns = patterns('profiles.views',
	
    # Examples:
    # url(r'^$', 'jumpstart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', 'settings', name='settings'),
    url(r'^edit/(?P<pk>[-_\w]+)$', 'settings_edit', name='settings_edit'),

)
