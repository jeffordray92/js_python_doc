import logging

from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from projects import (
    utils, 
    validators
)

from projects.exceptions import ProjectSetupError
from projects.models import (
    Project, 
    ProjectManagement, 
    ProjectRepository, 
    ProjectSetupStatus,
    ProjectTemplate,
    ProjectTestSite,
    ProjectType,
)

LOGGER = logging.getLogger('projects')
SETUP_OPTION_CHOICES = ((1, 'Setup a preview site for my project'),
                        (2, 'Setup JIRA project space'),
                        (3, 'Setup Redmine project space'))



class ProjectAddForm(forms.ModelForm):
    """
    This class handled the insertion of new Project instances.

    **Class Attributes:**
        * **name (str)**: refers to the project's name.\n
        * **description (str)**: short description about the project.\n
        * **company (str)**: company where project is affiliated to.\n
        * **project_type (radio)**: project type ranges in either Web or Mobile.\n
        * **project_template (radio)**: templates corresponding to a certain template.\n
        * **setup_option (multiplechoicefield)**: choices regarding as to what project tools to include to project.\n
        * **setup_test_site, setup_jira, setup_redmine (boolean)**: flag for setting up Project Management(PM) tools.

    """
    name             = forms.CharField(max_length=200, required=True, label="Project Name")
    description      = forms.CharField(widget=forms.Textarea, required=True, label="Project Description")
    company          = forms.CharField(max_length=200, required=False, label="Client Name")
    project_type     = forms.CharField(widget=forms.RadioSelect, required=True, label="Project Type")
    project_template = forms.CharField(widget=forms.RadioSelect, required=True, label="Project Template")
    setup_option     = forms.MultipleChoiceField(required=False,
                                                 widget=forms.CheckboxSelectMultiple, 
                                                 choices=SETUP_OPTION_CHOICES)
    setup_test_site  = False
    setup_jira       = False
    setup_redmine    = False

    class Meta:
        model  = Project
        fields = ('name', 'description', 'company', 'project_type', 'project_template')

    def clean(self):
        # Assign appropriate model object to  project_type and project_template
        if self.cleaned_data.get('project_type'):
            self.cleaned_data['project_type'] =  ProjectType.objects.get(pk=self.cleaned_data.get('project_type'))
            print self.cleaned_data['project_type']

        if self.cleaned_data.get('project_template'):
            self.cleaned_data['project_template'] = ProjectTemplate.objects.get(pk=self.cleaned_data.get('project_template'))
            print self.cleaned_data['project_template']

        # Retrieve user setup options selection
        setup_choices = self.cleaned_data.get('setup_option')
        self.setup_test_site =  '1' in setup_choices
        self.setup_jira =  '2' in setup_choices
        self.setup_redmine =  '3' in setup_choices

        return self.cleaned_data

    def clean_name(self):
        """
        Validates project's ``name`` if a project with the same name already exists.

        """
        project_name = self.cleaned_data['name']
        if Project.objects.filter(slug=slugify(project_name)).exists():
            LOGGER.error("A Project with the same name already exists. (project name: %s)" % project_name)
            raise forms.ValidationError(u"A Project with the same name already exists.")
        return project_name

    def init_project(self):
        """
        Create new records with initial data for :py:class:`ProjectRepository`, :py:class:`ProjectManagement` and :py:class:`ProjectTestSite` objects.

        ::

          self.project_repository = ProjectRepository.objects.create(project=project)
          self.project_test_site = ProjectTestSite.objects.create(project=project)
          self.pm_tool_jira = self.init_pm_tool(project, ProjectManagement.JIRA, not self.setup_jira)
          self.pm_tool_redmine = self.init_pm_tool(project, ProjectManagement.REDMINE, not self.setup_redmine)

        """
        project = self.instance

        #Create record for ProjectRepository with initial status=NEW
        self.project_repository = ProjectRepository.objects.create(project=project)

        #Create record for ProjectTestSite with initial status=NEW
        self.project_test_site = ProjectTestSite.objects.create(project=project)
        self.skip_setup(self.project_test_site, not self.setup_test_site)

        #Create record for ProjectManagement with initial status=NEW or SKIP (if specified by user)
        self.pm_tool_jira = self.init_pm_tool(project, ProjectManagement.JIRA, not self.setup_jira)
        self.pm_tool_redmine = self.init_pm_tool(project, ProjectManagement.REDMINE, not self.setup_redmine)
        
    def init_pm_tool(self, project, pm_tool_type, skip):
        """
        Responsible for initializing the project management tool selected.

        :param project: The current :py:class:`Project` instance.
        :param pm_tool_type: Refers to the PM tool selected
        :param skip: Flag if specified PM tool is to be set up or not.

        Creates a :py:class:`ProjectManagement` object given the following parameters.
        The resulting object is then passed as a parameter to :py:func:`skip_setup()`.

        :returns: :py:class:`ProjectManagement` object

        """
        pm_tool = ProjectManagement.objects.create(project=project, pm_tool=pm_tool_type)
        self.skip_setup(pm_tool, skip)
        return pm_tool

    def skip_setup(self, model, skip):
        """
        Checks if the creation of the specified PM tool is skipped.\n
        Calls :py:func:`projects.utils.update_setup_status_skip()` to update its status.
        """
        if skip:
            utils.update_setup_status_skip(model)

    def create_project(self, user):
        """
        This function is responsible for the backend processing of the automated project creation.
        It handles both the initialization of the project and its corresponding project tools.

        :param user: contains the credentials of the currently logged user which will be used to link to its corresponding project.
        
        Raises: :py:class:`ProjectSetupError`

        ::

          self.init_project()

        The :py:func:`init_project()` function is called to start creation process. It is responsible for creating records related to the project (see its section for more details).

        Afterwhich it calls four (4) functions from the ``utils`` module which handles the creation/setup of the project tools specified by the user.
        ::

          utils.setup_repository(self.project_repository, user)
          utils.setup_test_site(self.project_test_site, self.project_repository)
          utils.setup_jira_space(self.pm_tool_jira)
          utils.setup_redmine_space(self.pm_tool_redmine, user)

        Refer to :py:mod:`projects.utils` module for more details regarding each project tool's function.

        :returns: ``True`` if successfully initialized, otherwise ``False``.

        """
        try:
        
            # Create a record for Project
            self.save()

            # Create new records with initial data for ProjectRepository, ProjectManagement and ProjectTestSite
            self.init_project()
            
            # Setup BitBucket repository and store details in ProjectRepository
            utils.setup_repository(self.project_repository, user)

            # Setup the test site for the new project and store details in ProjectTestSite
            # (if option is checked by user)
            if self.setup_test_site:
                utils.setup_test_site(self.project_test_site, self.project_repository)

            # Setup JIRA project space for the new project and store details in ProjectManagement
            # (if option is checked by user)        
            if self.setup_jira:
                utils.setup_jira_space(self.pm_tool_jira)

            # Setup REDMINE project space for the new project and store details in ProjectManagement
            # (if option is checked by user)        
            if self.setup_redmine:
                utils.setup_redmine_space(self.pm_tool_redmine, user)

            return True

        except ProjectSetupError as project_setup_error:
            # TODO Log error and display to screen
            LOGGER.error("Project setup failed. (%s)" % project_setup_error)
            return False;

    def project_type_pk(self):
        return self.instance.project_type.pk

    def project_types(self):
        return ProjectType.objects.all()

    def project_type_web_selected(self):
        return self.project_type_pk() == 1

    def project_type_mobile_selected(self):
        return self.project_type_pk() == 2

    def project_template_pk(self):
        return self.instance.project_template.pk

    def project_template_selected(self):
        return self.project_template_pk()

    def project_templates_web(self):
        return ProjectTemplate.objects.filter(project_type=1)

    def project_templates_mobile(self):
        return ProjectTemplate.objects.filter(project_type=2)


class ProjectEditForm(forms.ModelForm):
    """
    Handles the editing of :py:class:`Project` objects.

    *Class Variables*
        * **company (str)**: company where project is affiliated to.\n
    """

    company = forms.CharField(required=False)

    class Meta:
        model = Project
        fields = ('name', 'description', 'company')
        widgets = {'description':forms.Textarea(attrs={'rows':3})}
