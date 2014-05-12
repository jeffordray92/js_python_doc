"""

The **profiles.views.py** file involves classes that take a Web request and return a Web response.

"""
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from braces.views import LoginRequiredMixin

from profiles.models import Settings



class SettingsEditView(LoginRequiredMixin, UpdateView):
    """This process the Web request of editing the current fields in the Profiles model, thus updating the current user settings.

    **Arguments:**
        * LoginRequiredMixin: A mixin meant to redirect to the Login Page, once the user was not yet authenticated
        * UpdateView: A generic view, imported from django.views.generic, meant to edit details of the Profiles model

    **Fields:**
        * model: ``model = Settings``
        * template_name: ``template_name = '*profiles/settings_update.html*'``
        * login_url: ``login_url = '*/login/*'``

    """
    model = Settings
    template_name = 'profiles/settings_update.html'
    login_url = '/login/'

    def get_success_url(self):
        """Returns the display for the edited user settings.

        """
        return reverse('profiles:settings')

class SettingsView(LoginRequiredMixin, DetailView):
    """This process the Web request of presenting the current user settings.

    **Arguments:**
        * LoginRequiredMixin: A mixin meant to redirect to the Login Page, once the user was not yet authenticated
        * DetailView: A generic view, imported from django.views.generic, meant to display details of the Profiles model

    **Fields:**
        * model: ``model = Settings``
        * context_object_name: ``context_object_name = '*admin_settings*'``
        * template_name: ``template_name = '*profiles/settings_detail.html*'``
    """

    model = Settings
    context_object_name = 'admin_settings'
    template_name = 'profiles/settings_detail.html'

    def get_object(self, queryset=None):
        """Returns the object containing the settings information from the Database

        """
        user = self.request.user
        obj = Settings.objects.get(user=user)
        fields = {}
        for field in self.model._meta.fields:
            fields[field.name] = field.verbose_name
        obj.fields = fields
        return obj


settings = SettingsView.as_view()
settings_edit = SettingsEditView.as_view()
