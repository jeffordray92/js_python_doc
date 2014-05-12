"""

The **jumpstart.forms.py** file configures the editable forms (*interface for User Input*) to be used by the project, in general

"""
import logging
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

LOGGER = logging.getLogger('jumpstart')


class LoginForm(forms.Form):
    """Sets up the Login Form, by which the user would input their authentication details

    **Attributes:**

        * username: ``username = forms.CharField(label='Username', required=True)``
        * password: ``password = forms.CharField(label='Password', widget=forms.PasswordInput)``

    """


class LoginForm(forms.Form):

    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None
        self.request = request

    def clean(self):
        """Implements individual field check for the login information, and returns an error message once an invalid input is detected.

        **Raises:**

            * Validation error (*for non-existing usernames*):
                ``<username> does not exist. You must register first.``
            * Validation error (*for invalid username or password*):
                ``Your username/password is incorrect.``

        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if not user:
                LOGGER.error("User '%s', does not exist.", username)
                raise forms.ValidationError("'%s' does not exist. You must register first." % username)
            else:
                user = authenticate(username=username, password=password)
                if user:
                    self.user = user
                else:
                    LOGGER.error("Username/Password combination is incorrect. [Username:%s]", username)
                    raise forms.ValidationError('Your username/password is incorrect.')

    def login(self):
        """Implements the *login* method from *django.contrib.auth* and checks if the user is authenticated or not

        **Raises:**

            * Validation error (*for errors in logging*):
                ``User is not authenticated`` 
        """
        if self.user and self.user.is_active:
            login(self.request, self.user)
        else:
            LOGGER.warning("User is not authenticated. (user: %s)" % self.user.username)
            raise forms.ValidationError('User is not authenticated.')
