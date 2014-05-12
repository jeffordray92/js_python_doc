from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.generic import (
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin

from .forms import ProjectEditForm, ProjectAddForm
from .models import Project
from .utils import project_setup_retry
from profiles.models import Settings


class ProjectAddView(LoginRequiredMixin, FormView):
    template_name = "projects/project_add_form.html"
    form_class = ProjectAddForm
    
    def post(self, request, *args, **kwargs):
        self.show_results = False
        form = ProjectAddForm(self.request.POST or None)
        if form.is_valid():
            self.show_results = True
            success = form.create_project(request.user)   
            redirect_kwargs = {'id':form.instance.id,
                               'slug':form.instance.slug,
                               'setup_type':"project",
                               'success': success and "success" or "fail"}
            return HttpResponseRedirect(reverse('project_details', kwargs=redirect_kwargs))
        return render(request, 'projects/project_add_form.html', {'form': form})

add = ProjectAddView.as_view()


class ProjectEditView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectEditForm
    template_name = 'projects/project_edit_form.html'

    def get_object(self, queryset=None):
        return Project.objects.get(id=self.kwargs['id'], slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('projects')

edit = ProjectEditView.as_view()


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'project_list'
    paginate_by = settings.DEFAULT_PAGINATION
    queryset = Project.objects.order_by('-created')

project_list = ProjectListView.as_view()


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_object(self, queryset=None):
        return Project.objects.get(id=self.kwargs['id'], slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['setup_type'] = self.kwargs.get('setup_type','')
        success = self.kwargs.get('success','')
        if (success == 'success'):
            context['success'] = True
        return context

    def post(self, request, *args, **kwargs):
        project_id = request.POST.get('project_id', '')
        project_slug = request.POST.get('project_slug', '')
        setup_type = request.POST.get('setup_type', '')

        if project_id and project_slug and setup_type:
            success = project_setup_retry(project_id, setup_type, request.user) and "success" or "fail";
            url = reverse('project_details', kwargs={'id':project_id,
                                                     'slug':project_slug,
                                                     'setup_type':setup_type,
                                                     'success':success})
            return HttpResponseRedirect(url)

        return HttpResponseRedirect("#")

details = ProjectDetailView.as_view()
