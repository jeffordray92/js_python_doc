"""

The **jumpstart.views.py** file involves classes that take a Web request and return a Web response.

"""
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import (
    HttpResponse, 
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.views.generic import (
    DetailView,
    TemplateView,
)
from django.views.generic.edit import FormMixin

from .forms import LoginForm

from django.shortcuts import render_to_response



class HomePageView(TemplateView):
    """This process the Web request of viewing the Home Page

    **Fields:**
        * template_name: ``template_name = u"home.html"``
        * page_slug: ``page_slug = u""``
        * page_title: ``page_title = u"JumpStart"``

    """
    template_name = u"home.html"
    page_slug = u""
    page_title = u"JumpStart"

home = HomePageView.as_view()


class LoginView(FormMixin, DetailView):
    """This process the Web request of presenting the Login page and starts a session using the user's account

    **Fields:**
        * form_class: ``form_class = LoginForm``
            .. |LoginForm| replace:: :class:`jumpstart.forms.LoginForm`
            .. |jumpstart.forms| replace:: :mod:`jumpstart.forms`

            This utilizes the |LoginForm| initialized in the |jumpstart.forms| module
        * template_name: ``template_name = 'login.html'``

    """
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        """Gets the username and password entered by the user

        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        login_form = LoginForm(request)
        login_form.redirect_to = request.REQUEST.get('next', reverse('home'))
        return render(request, self.template_name, {'form': login_form})

    def post(self, request, *args, **kwargs):
        """.. |get| replace:: :func:`jumpstart.views.LoginView.get`

        Submits the username and password from the |get| method, authenticates if it is valid, and starts a new session

        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        login_form = LoginForm(request, request.POST)
        if login_form.is_valid():
            login_form.login()
            redirect_to = request.REQUEST.get('next', reverse('home'))
            return HttpResponseRedirect(redirect_to)
        return render(request, self.template_name, {'form': login_form})

login = LoginView.as_view()


class LogoutView(TemplateView):
    """This process the Web request of presenting the logging out the user and ending its current session

    """

    def get(self, request, *args, **kwargs):
        """.. |home| replace:: :func:`jumpstart.views.HomePageView`

        Logs the user out, ends the current session, and redirects to |home|.

        """
        auth.logout(request)
        return HttpResponseRedirect(reverse('home'))
        
logout = LogoutView.as_view()


class Wiki_View(TemplateView):
    """This process the Web request of viewing the Wiki Page

    **Returns:**
        * Redirects to ``wiki/index.html``

    """
    template_name = u"wiki/index.html"

wiki = Wiki_View.as_view()

class errorview(TemplateView):
    template_name = u"error404.html"
    page_slug = u""
    page_title = u"ERROR!"

error = errorview.as_view()