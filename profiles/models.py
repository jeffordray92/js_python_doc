"""

The **profiles.models.py** file includes the models -- the definitive source of information about your data -- included in the project.

.. NOTE::
   In this set of codes, each attribute of the model represents a specific field in the database.

"""

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import validate_slug

from profiles.validators import (
    validate_alphanumeric,
    validate_exclude_space,
    validate_not_spaces
)


class Settings(models.Model):


    """Provides attributes for the user information and other settings specifications

    **Attributes:**

    #. Foreign Keys:

        * user: ``user = models.ForeignKey(User)``
            Taken from *django.contrib.auth.models*, *user* signifies that the settings provided are applicable to this certain user.

    #. Project Repository (Bitbucket) Access and Authentication:

        * repository_username: ``repository_username = *models.CharField(max_length=200, null=True, verbose_name="Bitbucket Account", validators=[validate_not_spaces, validate_exclude_space])*``
            Signifies the username for the Bitbucket account where the project will initially be pushed
        * repository_consumer_key: ``repository_consumer_key = *models.CharField(max_length=200, null=True, verbose_name="Consumer Key", validators=[validate_not_spaces, validate_alphanumeric])*``
            The BitBucket consumer key that the BitBucket API use to identify the user
        * repository_oauth_access_token: ``repository_oauth_access_token = models.CharField(max_length=200, null=True, blank = True, verbose_name="OAuth Access Token", validators=[validate_not_spaces, validate_alphanumeric])``
            With this access token, the project can make Bitbucket API calls
        * repository_oauth_access_token_secret: ``repository_oauth_access_token_secret = models.CharField(max_length=200, null=True, blank = True, verbose_name="OAuth Token Secret", validators=[validate_not_spaces, validate_alphanumeric])``
            Used to verify the repository_oauth_access_token
        * ssh_host_alias: ``ssh_host_alias = models.CharField(max_length=200, null=True, blank = True, verbose_name="SSH Host Alias", validators=[validate_not_spaces, validate_exclude_space])``
            The alias name for the SSH host to be used for pushing the project with Bitbucket
        * test_repository_slug: ``test_repository_slug = models.CharField(max_length=200, null=True, verbose_name="Test Repository Slug", validators=[validate_not_spaces, validate_slug])``
            The slug which will be used to identify the project in the Bitbucket URL, once it is pushed.
        * projects_working_directory: ``projects_working_directory = models.CharField(max_length=200, null=True, verbose_name="Projects Working Directory", help_text=HELP_TEXT_HOME, validators=[validate_not_spaces])``
            The local directory by which the project will be used
        * default_project_folder_name: ``default_project_folder_name = models.CharField(max_length=200, null=True, verbose_name="Default Project Folder Name (to be replaced)", validators=[validate_not_spaces, validate_exclude_space])``
            The default name of the project folder

    #. Jira Project Management:

        * jira_key: ``jira_key = models.TextField(null=True, blank = True, verbose_name="Jira Key", validators=[validate_not_spaces, validate_alphanumeric])``
            The specific project key to be used by JIRA to identify the project space

    #. Redmine Project Management:

        * redmine_key: ``redmine_key = models.CharField(max_length=200, null=True, blank = True, verbose_name="API Access Key", validators=[validate_not_spaces, validate_alphanumeric])``
            The specific project key to be used by Redmine to identify the project space
        * redmine_url: ``redmine_url = models.URLField(null=True, blank = True, verbose_name="Redmine Environment URL", validators=[validate_not_spaces])``
            The URL of the Redmine account of the user, where the project space will be created

    **Constants:**

        * HELP_TEXT_HOME: ``HELP_TEXT_HOME = "This is a directory under $HOME (/home/username/)"``
            Default string message, indicating the Home directory


    """
    
    # Constants
    HELP_TEXT_HOME = "This is a directory under $HOME (/home/username/)"

    # Below settings applicable to this user
    user = models.ForeignKey(User)
    
    # Project repository (Bitbucket) Access and Authentication
    repository_username = models.CharField(max_length=200, null=True, verbose_name="Bitbucket Account", validators=[validate_not_spaces, validate_exclude_space])
    repository_consumer_key = models.CharField(max_length=200, null=True, verbose_name="Consumer Key", validators=[validate_not_spaces, validate_alphanumeric])
    repository_consumer_secret = models.CharField(max_length=200, null=True, verbose_name="Consumer Secret", validators=[validate_not_spaces, validate_alphanumeric])
    repository_oauth_access_token = models.CharField(max_length=200, null=True, blank = True, verbose_name="OAuth Access Token", validators=[validate_not_spaces, validate_alphanumeric])
    repository_oauth_access_token_secret = models.CharField(max_length=200, null=True, blank = True, verbose_name="OAuth Token Secret", validators=[validate_not_spaces, validate_alphanumeric])
    ssh_host_alias = models.CharField(max_length=200, null=True, blank = True, verbose_name="SSH Host Alias", validators=[validate_not_spaces, validate_exclude_space])
    test_repository_slug = models.CharField(max_length=200, null=True, verbose_name="Test Repository Slug", validators=[validate_not_spaces, validate_slug])
    projects_working_directory = models.CharField(max_length=200, null=True, verbose_name="Projects Working Directory", help_text=HELP_TEXT_HOME, validators=[validate_not_spaces])
    default_project_folder_name = models.CharField(max_length=200, null=True, verbose_name="Default Project Folder Name (to be replaced)", validators=[validate_not_spaces, validate_exclude_space])
    
    # Jira Project Management
    jira_key = models.TextField(null=True, blank = True, verbose_name="Jira Key", validators=[validate_not_spaces, validate_alphanumeric])
    
    # Redmine Project Management
    redmine_key = models.CharField(max_length=200, null=True, blank = True, verbose_name="API Access Key", validators=[validate_not_spaces, validate_alphanumeric])
    redmine_url = models.URLField(null=True, blank = True, verbose_name="Redmine Environment URL", validators=[validate_not_spaces])
    
    # Test Site Deployment    
    domain_host = models.CharField(max_length=200, null=True, blank = True, verbose_name="Domain Host", validators=[validate_not_spaces])
    domain_user = models.CharField(max_length=200, null=True, blank = True, verbose_name="Domain User", validators=[validate_not_spaces, validate_exclude_space])
    domain_path = models.CharField(max_length=200, null=True, blank = True, verbose_name="Domain Project Root", help_text=HELP_TEXT_HOME, validators=[validate_not_spaces])
