from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from model_utils.models import TimeStampedModel

from projects.validators import validate_alphanumeric, validate_not_spaces



class ProjectType(models.Model):
    """
    Class for the project's *type*.

    **Class Attributes:**
        * **name (str)**: project type's name\n
        * **description (str)**: project type's short description\n

    """
    name             = models.CharField(max_length=200) 
    description      = models.TextField() 
    
    def __unicode__(self):
        return "%s - %s" % (self.name, self.description)


class ProjectTemplate(models.Model):
    """
    Class for the project's *templates*.

    **Class Attributes:**
        * **name (str)**: project templates's name.\n
        * **description (str)**: project templates's short description.\n
        * **project_type (fk)**: project template to base on given project type.\n
        * **repo_https (url)**: Bitbucket repository's HTTPS url.\n
        * **repo_ssh (str)**: Bitbucket repository's SSH url.\n
        
    """
    name         = models.CharField(max_length=200) 
    description  = models.TextField() 
    project_type = models.ForeignKey(ProjectType)
    repo_https   = models.URLField()
    repo_ssh     = models.CharField(max_length=200) 

    def __unicode__(self):
        return "%s - %s" % (self.name, self.description)


class Project(TimeStampedModel):
    """
    Class for the *project*.

    **Class Attributes:**
        * **name (str)**: project type's name.\n
        * **description (str)**: project type's short description.\n
        * **company (str)**: company a project is affiliated to.\n
        * **project_type (fk)**: a project's type.\n
        * **project_template (fk)**: a project's template.\n
        * **slug (str)**: a project's slug value (for url usage).\n
        
    """
    name               = models.CharField(max_length=200, validators=[validate_alphanumeric, validate_not_spaces]) 
    description        = models.TextField(validators=[validate_not_spaces])
    company            = models.CharField(max_length=200, null=True, blank = True)
    project_type       = models.ForeignKey(ProjectType)
    project_template   = models.ForeignKey(ProjectTemplate)
    slug               = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.description)

    def get_absolute_url(self):
        """Returns a url for a specified project's detail page"""
        return reverse('project_details', kwargs={'id':self.id, 'slug':self.slug})

    def get_edit_url(self):
        """Returns a url for a specified project's edit page"""
        return reverse('project_edit', kwargs={'id':self.id, 'slug':self.slug})

    def get_project_repository(self):
        """Retrieves all :py:class:`ProjectRepository` objects"""
        return ProjectRepository.objects.all().get(project=self)

    def get_project_pm_tool_jira(self):
        """Retrieves all `JIRA` :py:class:`ProjectManagement` objects"""
        return ProjectManagement.objects.all().get(project=self, pm_tool=ProjectManagement.JIRA)

    def get_project_pm_tool_redmine(self):
        """Retrieves all `Redmine` :py:class:`ProjectManagement` objects"""
        return ProjectManagement.objects.all().get(project=self, pm_tool=ProjectManagement.REDMINE)

    def get_project_test_site(self):
        """Retrieves all :py:class:`ProjectTestSite` objects"""
        return ProjectTestSite.objects.all().get(project=self)


class ProjectSetupStatus(TimeStampedModel):
    """
    Class for the project's *setup status*.

    **Constants:**
    ::

      NEW = 'N'
      SKIP = 'S'
      WORKING = 'W'
      FAILED = 'F'
      DONE = 'D'
      STATUS_CHOICES = (
          (NEW, 'New'),
          (SKIP, 'Skip'),
          (WORKING, 'Working'),
          (FAILED, 'Failed'),
          (DONE, 'Done'),
      )

    **Class Attributes:**
        * **status (str)**: project type's name. Based on ``STATUS_CHOICES``.\n
        * **url (url)**: project status' url.\n
        * **remarks (str)**: status' remarks.\n
        
    """
    NEW = 'N'
    SKIP = 'S'
    WORKING = 'W'
    FAILED = 'F'
    DONE = 'D'
    STATUS_CHOICES = (
        (NEW, 'New'),
        (SKIP, 'Skip'),
        (WORKING, 'Working'),
        (FAILED, 'Failed'),
        (DONE, 'Done'),
    )
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default=NEW)
    url = models.URLField(null=True)
    remarks = models.TextField(null=True)
    
    class Meta:
        abstract = True

    def is_success(self):
        """Returns a ``Done`` status."""
        return self.status == self.DONE

    def is_failed(self):
        """Returns a ``Failed`` status."""
        return self.status in (self.FAILED, self.WORKING)

    def is_skipped(self):
        """Returns a ``Skip`` status."""
        return self.status in (self.SKIP, self.NEW)


class ProjectRepository(ProjectSetupStatus):
    """
    Class for the project's setup status.

    **Class Attributes:**
        * **project (fk)**: :py:class:`Project` instance.\n
        * **repo_https (url)**: Bitbucket repository's HTTPS url.\n
        * **repo_ssh (str)**: Bitbucket repository's SSH url.\n

    """
    project    = models.ForeignKey(Project)
    repo_https = models.URLField(null=True)
    repo_ssh   = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.repo_https, self.repo_ssh)


class ProjectManagement(ProjectSetupStatus):
    """
    Class for the project's setup status.

    **Constants:**
    ::

      JIRA = 'J'
      REDMINE = 'R'
      PM_TOOL_CHOICES = (
          (JIRA, 'Jira'),
          (REDMINE, 'Redmine'),
      )'

    *Class Attributes:*
        * **project (fk)**: :py:class:`Project` instance.\n
        * **pm_tool (str)**: PM tool to be used. Based on ``PM_TOOL_CHOICES``.\n

    """
    JIRA = 'J'
    REDMINE = 'R'
    PM_TOOL_CHOICES = (
        (JIRA, 'Jira'),
        (REDMINE, 'Redmine'),
    )
    project = models.ForeignKey(Project)
    pm_tool = models.CharField(max_length=1, choices=PM_TOOL_CHOICES)

    def __unicode__(self):
        return "%s" % (self.url)

    
class ProjectTestSite(ProjectSetupStatus):
    """Class for the `test-site`

    **Class Attributes:**
        * **project (fk):** :py:class:`Project` instance.\n

    """
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "%s" % (self.url)
