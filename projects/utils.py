import fileinput
import logging
import os
import subprocess
import sys
import shutil
import webbrowser

from django.http import HttpResponse
from django.shortcuts import render_to_response
from urlparse import urljoin

from bitbucket.bitbucket import Bitbucket
from redmine import Redmine

from profiles.models import Settings
from projects.exceptions import ProjectSetupError
from projects.models import (
    Project, 
    ProjectManagement, 
    ProjectRepository, 
    ProjectSetupStatus,
    ProjectTestSite,
)

USER_HOME = os.path.expanduser('~')
REPOSITORY_HOST = "bitbucket.org"
LOGGER = logging.getLogger("projects")



def setup_repository(project_repository, user):
    """
    Handles all the repository-related functions necessary for the creation of project's repository.

    :param project_repository: A newly initialized :py:class:`ProjectRepository` object linked to the current project in progress.
    :param user: Currently logged in user.

    :returns: `True` if setup was successfully created

    Raises: :py:class:`ProjectSetupError`

    Initially, it sets the :py:func:`update_setup_status_working()` for the ``project_repository``.
    Before the setup, it authorizes the Bitbucket account used by Jumpstart, where it will store the new repository that will be created by the user.
    ::

      bitbucket = authorize_bitbucket(settings)

    where ``settings`` contains all the settings *(keys, urls)* that will be used to setup the project tools. (see :py:func:`authorize_bitbucket()`)

    Next, a repository that corresponds to the template chosen is then cloned using :py:func:`clone_template()`.

    Given all the necessary configurations *(authorize, clone, rename template)* have been completed, the project's
    repository can now be created by calling :py:func:`create_new_repository()`.

    Once the repository has been successfully created, it then updates the status of the ``project_repository``.

    ::

      update_setup_status_done(project_repository)

    """
    try:
        # Start creating project repository (set status=WORKING)
        update_setup_status_working(project_repository)

        project = project_repository.project
        settings = Settings.objects.all().get(user=user)

        # Set current project's working directory
        projects_relative_directory = settings.projects_working_directory
        projects_working_directory = os.path.join(USER_HOME, projects_relative_directory.startswith(os.sep) and projects_relative_directory[1:] or projects_relative_directory)
        project_working_directory = os.path.join(projects_working_directory, str(project.id) + "-" + project.slug)
        
        if not os.path.isdir(project_working_directory):
            os.makedirs(project_working_directory)
        bitbucket = authorize_bitbucket(settings)

        # Clone template from template repository
        default_project_folder_name = settings.default_project_folder_name
        project_folder_name = project.slug.replace("-", "_")
        project_template_ssh = set_ssh_host_alias(project.project_template.repo_ssh, REPOSITORY_HOST, settings.ssh_host_alias)
        project_base_directory = clone_template(project_working_directory, settings.default_project_folder_name, project_folder_name, project_template_ssh)

        # Create NEW Bitbucket Project Repository (Initial commit, based on template selected)
        create_new_repository(bitbucket, project, project_repository, project_working_directory, settings.ssh_host_alias)

        # Done creating repository (set status=DONE)
        update_setup_status_done(project_repository)

        return True;

    except ProjectSetupError as project_setup_error:
        error_message =  "%s (%s)" % (str(project_setup_error), type(project_setup_error))
        LOGGER.error("%s (user: %s, project name: %s, bitbucket: %s)" % (error_message, user, project_folder_name, bitbucket))
        update_setup_status_failed(project_repository, project_setup_error.value)
        raise ProjectSetupError("Failed to create New Bitbucket Repository.")

def authorize_bitbucket(settings):
    """
    Handles the authorization of Jumpstart's Bitbucket account to allow access to its repository.
    It needs to be authorized since the system will push the project to its repository. 

    .. seealso:: :py:func:`create_new_repository()`

    :param settings: Contains the necessary keys that will be used for Bitbucket authorization

    :returns: an *authorized* :py:class:`Bitbucket` object

    Raises: :py:class:`ProjectSetupError`
    
    ::

      bitbucket = Bitbucket(bitbucket_username)

    where ``bitbucket_username`` refers the Jumpstart's Bitbucket username.

    .. note:: :py:class:`Bitbucket` is from Python's `Bitbucket API library <https://pypi.python.org/pypi/bitbucket-api>`_.

    """
    
    # [Paul] Notes on Bitbucket API:
    
    # Bitbucket.authorize() always returns True if all parameters are provided (even if incorrect! -- see code in link below)
    # Actual verification of oauth credentials only done upon sending of GET request in the following Repository class methods:

    #     Repository.all()
    #     Repository.get()*
    #     Repository.create()
    #     Repository.update()
    #     Repository.delete()
    #     Repository.archive()
     
    # *Hence, we create a blank TEST_REPOSITORY to verify if our succeeding actions can push through via the Bitbucket API
    #  (better than calling Repository.all())
    
    # Reference source code:
    #     Bitbucket class - https://bitbucket-api.readthedocs.org/en/latest/_modules/bitbucket/bitbucket.html
    #     Repository class - https://bitbucket-api.readthedocs.org/en/latest/_modules/bitbucket/repository.html

    TEST_REPOSITORY_SLUG = settings.test_repository_slug

    bitbucket_username = settings.repository_username
    bitbucket_consumer_key = settings.repository_consumer_key
    bitbucket_consumer_secret = settings.repository_consumer_secret
    bitbucket_oauth_access_token = settings.repository_oauth_access_token
    bitbucket_oauth_access_token_secret = settings.repository_oauth_access_token_secret
 
    # Bitbucket OAuth Authentication
    bitbucket = Bitbucket(bitbucket_username)

    if not bitbucket_oauth_access_token and not bitbucket_oauth_access_token_secret:
        
        bitbucket.authorize(bitbucket_consumer_key, bitbucket_consumer_secret, 'http://127.0.0.1:8000/')
        
        # Open a webbrowser and get the token
        webbrowser.open(bitbucket.url('AUTHENTICATE', token=bitbucket.access_token))
        
        # Copy the verifier field from the URL in the browser into the console
        oauth_verifier = raw_input('Enter verifier from url [oauth_verifier]')
        success, result = bitbucket.verify(oauth_verifier)
        
        if not success:
            LOGGER.warning("OAuth verification with Bitbucket repository failed. Could not proceed. Please check the Consumer Key and Consumer Secret provided in the Settings page. (bitbucket: %s, bitbucket username: %s)" % (error_message, bitbucket, bitbucket_username))
            raise ProjectSetupError("%s" % error_message)

        settings.repository_oauth_access_token = bitbucket.access_token
        settings.repository_oauth_access_token_secret = bitbucket.access_token_secret
        settings.save()

    else:    
        
        bitbucket.authorize(bitbucket_consumer_key, bitbucket_consumer_secret, 'http://127.0.0.1:8000/', bitbucket_oauth_access_token, bitbucket_oauth_access_token_secret)

    # Test repository accessibility via Bitbucket API
    #test_repository_slug = settings.test_repository_slug ---> still to be added in Settings model
    success, test_repository = bitbucket.repository.get(TEST_REPOSITORY_SLUG)

    if not success:
        # failed to establish connection to the repository. cannot proceed. prompt for retry.
        LOGGER.warning("Authentication with Bitbucket repository failed. Could not proceed. (bitbucket: %s, bitbucket username: %s)" % (error_message, bitbucket, bitbucket_username))
        raise ProjectSetupError("%s" % error_message)

    return bitbucket

def clone_template(project_working_directory, default_project_folder_name, project_folder_name, project_template_ssh):
    """
    This is where the template is cloned from Jumpstart's repository.

    :param project_working_directory: Path where the cloned template is located.
    :param default_project_folder_name: The default name for the project's folder.
    :param project_template_ssh: The Bitbucket SSH key to be used for cloning the template.

    Raises: :py:class:`ProjectSetupError`

    Cloning of the template is executed by running a command at the terminal using :py:func:`subprocess.call()`.
    ::

      return_code = subprocess.call(clone_template_command, shell=True)

    where ``return_code`` stores the status of the called command, and ``clone_template_command`` 
    is a pre-defined command that executes *git clone*.

    .. note:: You can visit `The official Documentation of
     Git <http://git-scm.com/book/en/Git-Basics-Getting-a-Git-Repository>`_ for a better understanding of `git clone` and other related commands.

    Two other functions are called to finish the process of cloning the project template, 
    the :py:func:`change_project_name()` and :py:func:`create_superuser_fixtures()`.

    """

    clone_template_command = 'git clone %s %s' % (project_template_ssh, project_working_directory)
    print clone_template_command
    
    try:
        return_code = subprocess.call(clone_template_command, shell=True)
        
        if return_code < 0:
            LOGGER.error("Cloning of template failed. Could not proceed. Child was terminated by signal. (return code: %s, template ssh: %s, directory: %s)" % (return_code, project_template_ssh, project_working_directory))
            raise ProjectSetupError("Cloning of template failed. Could not proceed. [Return code: " + str(-return_code) + "]")

        change_project_name(project_working_directory, default_project_folder_name, project_folder_name)

        project_base_directory = os.path.join(project_working_directory, project_folder_name)
        
        create_superuser_fixtures(project_base_directory)   

    except OSError as os_error:
        LOGGER.error("Cloning of template failed. Could not proceed. (Execution failed: %s)" % os_error)
        raise ProjectSetupError("Cloning of template failed. Could not proceed. [Exception: " + str(os_error) + "]")

def change_project_name(base_directory, default_project_folder_name, project_folder_name):
    """
    Renames the default `project_name` of the cloned template folder into the actual project's name.

    :param base_directory: Path where the cloned template is located.
    :param default_project_folder_name: The default name for the project's folder.
    :param project_folder_name: Serves as the new folder name of the template.

    """
    # INFO: it also traverses the ../.git/ directory. Should we skip or ok?
    for file_name in os.listdir(base_directory):
        file_path = os.path.join(base_directory, file_name)
        if os.path.isdir(file_path):
            change_project_name(file_path, default_project_folder_name, project_folder_name)
            if default_project_folder_name == os.path.basename(file_path):
                new_project_folder_path = os.path.join(base_directory, project_folder_name)
                os.renames(file_path, new_project_folder_path)
        elif file_name.endswith('.py'):
            for line in fileinput.input(file_path, inplace=True):
                line = line.replace(default_project_folder_name, project_folder_name)
                sys.stdout.write(line)

def create_superuser_fixtures(project_base_directory):
    # [June] NOTE: might deprecate this depending on final template structure.
    # Might be easier and faster if superuser fixture was already included in template.

    """
    Creates a *superuser* to the database.
    """
    fixtures_directory = os.path.join(project_base_directory, "fixtures")
    if not os.path.exists(fixtures_directory):
        os.makedirs(fixtures_directory)
    initial_data_path = os.path.join(fixtures_directory, "initial_data.json")
    initial_data = open(initial_data_path, "wb")
    initial_data.write('[{"pk": 1, "model": "contenttypes.contenttype", "fields": {"model": "logentry", "name": "log entry", "app_label": "admin"}}, {"pk": 2, "model": "contenttypes.contenttype", "fields": {"model": "permission", "name": "permission", "app_label": "auth"}}, {"pk": 3, "model": "contenttypes.contenttype", "fields": {"model": "group", "name": "group", "app_label": "auth"}}, {"pk": 4, "model": "contenttypes.contenttype", "fields": {"model": "user", "name": "user", "app_label": "auth"}}, {"pk": 5, "model": "contenttypes.contenttype", "fields": {"model": "contenttype", "name": "content type", "app_label": "contenttypes"}}, {"pk": 6, "model": "contenttypes.contenttype", "fields": {"model": "session", "name": "session", "app_label": "sessions"}}, {"pk": 1, "model": "auth.permission", "fields": {"codename": "add_logentry", "name": "Can add log entry", "content_type": 1}}, {"pk": 2, "model": "auth.permission", "fields": {"codename": "change_logentry", "name": "Can change log entry", "content_type": 1}}, {"pk": 3, "model": "auth.permission", "fields": {"codename": "delete_logentry", "name": "Can delete log entry", "content_type": 1}}, {"pk": 4, "model": "auth.permission", "fields": {"codename": "add_permission", "name": "Can add permission", "content_type": 2}}, {"pk": 5, "model": "auth.permission", "fields": {"codename": "change_permission", "name": "Can change permission", "content_type": 2}}, {"pk": 6, "model": "auth.permission", "fields": {"codename": "delete_permission", "name": "Can delete permission", "content_type": 2}}, {"pk": 7, "model": "auth.permission", "fields": {"codename": "add_group", "name": "Can add group", "content_type": 3}}, {"pk": 8, "model": "auth.permission", "fields": {"codename": "change_group", "name": "Can change group", "content_type": 3}}, {"pk": 9, "model": "auth.permission", "fields": {"codename": "delete_group", "name": "Can delete group", "content_type": 3}}, {"pk": 10, "model": "auth.permission", "fields": {"codename": "add_user", "name": "Can add user", "content_type": 4}}, {"pk": 11, "model": "auth.permission", "fields": {"codename": "change_user", "name": "Can change user", "content_type": 4}}, {"pk": 12, "model": "auth.permission", "fields": {"codename": "delete_user", "name": "Can delete user", "content_type": 4}}, {"pk": 13, "model": "auth.permission", "fields": {"codename": "add_contenttype", "name": "Can add content type", "content_type": 5}}, {"pk": 14, "model": "auth.permission", "fields": {"codename": "change_contenttype", "name": "Can change content type", "content_type": 5}}, {"pk": 15, "model": "auth.permission", "fields": {"codename": "delete_contenttype", "name": "Can delete content type", "content_type": 5}}, {"pk": 16, "model": "auth.permission", "fields": {"codename": "add_session", "name": "Can add session", "content_type": 6}}, {"pk": 17, "model": "auth.permission", "fields": {"codename": "change_session", "name": "Can change session", "content_type": 6}}, {"pk": 18, "model": "auth.permission", "fields": {"codename": "delete_session", "name": "Can delete session", "content_type": 6}}, {"pk": 1, "model": "auth.user", "fields": {"username": "admin", "first_name": "", "last_name": "", "is_active": true, "is_superuser": true, "is_staff": true, "last_login": "2014-05-02T08:19:38.959Z", "groups": [], "user_permissions": [], "password": "pbkdf2_sha256$12000$XYuNBA5ije6y$FAMhxNddNQSIL9cE44DMWl6FjtORSlpwbgYvi+Vbmwc=", "email": "", "date_joined": "2014-05-02T08:19:38.959Z"}}]');
    initial_data.close()

def create_new_repository(bitbucket, project, project_repository, project_working_directory, ssh_host_alias):
    """
    Creates a new Bitbucket project repository. It also commits based on the project's template used.

    :param bitbucket: The authorized :py:class:`Bitbucket` object.
    :param project: The current project's instance.
    :param project_repository: A :py:class:`ProjectRepository` instance.
    :param project_working_directory: The directory of the template.
    :param ssh_host_alias: The host alias used for accessing Jumpstart's repository.

    Raises: :py:class:`ProjectSetupError`

    First, :py:class:`Bitbucket` checks if a repository with the same name as the project name has already been created.
    
    ::

      success, project_bitbucket_repository = bitbucket.repository.get(project_repository_slug)

    If no repository exists, then the ``repository.create()`` is called to create a repository into the Jumpstart's account.
    
    ::

      bitbucket.repository.create(project_repository_slug)

    where ``project_repository_slug`` is the desired name for the project repository.

    """

    # Check if bitbucket project with same identifier already exists
    project_repository_slug = project.slug
    success, project_bitbucket_repository = bitbucket.repository.get(project_repository_slug)

    if success:
        LOGGER.warning("Repository with the same identifier/name already exists. (project: %s, slug: %s)" % (project.name, project_repository_slug))
        raise ProjectSetupError("Repository with the same identifier/name already exists.")

    print 'creating new repository...'
    repository_created, project_bitbucket_repository = bitbucket.repository.create(project_repository_slug)

    if not repository_created:
        LOGGER.warning("Failed to create new repository. (project: %s, slug: %s)" % (project.name, project_repository_slug))
        raise ProjectSetupError("Failed to create new repository.")

    print 'new repository is created'
    bitbucket.repository.update(description=project.description)

    # Set the repository access details
    bitbucket_username = bitbucket.username
    project_repository.url = 'https://bitbucket.org/%s/%s' % (bitbucket_username, project_repository_slug)
    project_repository.repo_https = 'https://%s@bitbucket.org/%s/%s.git' % (bitbucket_username, bitbucket_username, project_repository_slug)
    project_repository.repo_ssh = 'git@bitbucket.org:%s/%s.git' % (bitbucket_username, project_repository_slug)

    try:
        repo_ssh = set_ssh_host_alias(project_repository.repo_ssh, REPOSITORY_HOST, ssh_host_alias) 
        command = "fab push:'%s,%s,%s'" % (project_working_directory, project.name, repo_ssh)
        return_code = subprocess.call(command, shell=True)
        
        if return_code < 0:
            LOGGER.warning("Pushing of project files to repository failed. Could not proceed. Fabfile execution terminated. (return code: %s)" % return_code)
            raise ProjectSetupError("Pushing of project files to repository failed. Could not proceed. [Return code: " + str(-return_code) + "]")

    except OSError as os_error:
        LOGGER.error("Creation of New Repository failed. Could not proceed. (Execution failed: %s)" % os_error)
        raise ProjectSetupError("Creation of New Repository failed. Could not proceed. [Exception: " + str(os_error) + "]")

    # Set the repository access details
    project_repository.save()

def set_ssh_host_alias(repo_ssh, repository_host, ssh_host_alias):
    # Replace REPOSITORY_HOST("bitbucket.org") with [SSH host alias] for multiple SSH keys or multiple bitbucket accounts
    """
    Replaces the default host (`bitbucket.org`) with `SSH Host Alias` to be used for accessing the repository.
 
    :param repo_ssh: The SSH Key of the repository.
    :param repository_host: The username of the Bitbucket account used.
    :param ssh_host_alias: Host alias used for multiple accounts.

    :returns: ``repo_ssh``

    .. note:: This is crucial for it will ensure users to be able to create a project and push the files to its corresponding repository, given that the user already has its own Bitbucket account(one that is not related to Jumpstart).For more information, please do read more about `SSH Host Alias <https://confluence.atlassian.com/pages/viewpage.action?pageId=271943168#ConfiguremultipleSSHidentitiesforGitBash,MacOSX,&Linux-CreatemultipleidentitiesforMacOSX,GitBash,andLinux>`_.

    """
    if ssh_host_alias:
        return repo_ssh.replace(repository_host, ssh_host_alias)
    return repo_ssh

def setup_test_site(project_test_site, project_repository, user):
    """
    Sets up a *test-site* for the project.

    :param project_test_site: The project's :py:class:`ProjectTestSite` instance.
    :param project_repository: The project's :py:class:`ProjectRepository` instance.
    :param user: Current user logged in.

    :returns: ``True`` if successful, otherwise ``False``.

    In creating the test site, the following command is called in the terminal using :py:func:`subprocess.call()`.

    ::

      command = "fab deploy:'%s,%s'" % (project_repo, project_name)
    """
    
    # start creating/setting-up test site
    update_setup_status_working(project_test_site)
    
    # TODO - Create/Setup test site
    settings = Settings.objects.all().get(user=user)
    project = project_test_site.project
    project_name = project.name
    project_name = project_name.replace (" ", "_")
    project_repo = set_ssh_host_alias(project_repository.repo_ssh, REPOSITORY_HOST, settings.ssh_host_alias)

    try:
        command = "fab deploy:'%s,%s'" % (project_repo, project_name)
        return_code = subprocess.call(command, shell=True)
        if return_code != 0:
            # failed to create test site - prompt for retry
            command = "fab rollback:'%s'" % project_name
            subprocess.call(command, shell=True)
            error_message =  "Fabric deployment failed. Test Site not created."
            LOGGER.error("%s (user: %s, return code: %s, project name: %s, project repo: %s, domain host: %s)" % (error_message, user, return_code, project_name, project_repo, settings.domain_host))
            update_setup_status_failed(project_test_site, error_message)
            return False

        # done creating test site
        project_test_site.url = "%s.%s" % (project_name, settings.domain_host)
        update_setup_status_done(project_test_site)
        return True            
    except OSError as os_error:
        # failed to create test site - prompt for retry
        command = "fab rollback:'%s'" % project_name
        subprocess.call(command, shell=True)
        error_message =  "%s (%s)" % (str(os_error), type(os_error))
        LOGGER.error("%s (user: %s, return code: %s, project name: %s, project repo: %s, domain host: %s)" % (error_message, user, return_code, project_name, project_repo, settings.domain_host))
        update_setup_status_failed(project_test_site, error_message)
        return False

def setup_jira_space(project_management):
    """
    Sets up *JIRA* project space

    :param project_management: The project's :py:class:`ProjectManagement` instance
    """
    
    # start creating/setting-up JIRA project space
    update_setup_status_working(project_management)
    
    # TODO - Create JIRA project space

    # done creating JIRA project space
    project_management.url = "http://www.test.com"
    update_setup_status_done(project_management)
    
    # failed to create JIRA project space - prompt for retry
    # update_setup_status_failed(project_management)

def setup_redmine_space(project_management, user):
    """
    Sets up *Redmine* project space.

    :param project_management: The project's :py:class:`ProjectManagement` instance.
    :param user: Current user logged in.

    :returns: ``True`` if setup was successful, otherwise ``False``

    First it retrieves the necessary `user's` credentials needed for Redmine in the :py:class:`Settings` module.

    Afterwhich, the Redmine's project space is now created using :py:class:`Redmine` from the `Redmine Python package`.

    ::

      redmine = Redmine(redmine_url, key=redmine_key, version='2.3.3', requests={'verify': False})
      redmine_project = redmine.project.create(name=project_name, identifier=project_identifier, description=project_description)

    where ``redmine_url`` and ``redmine_key`` are all retrieved from the user's :py:class:`Settings`.

    .. note:: Visit `Python-Redmine <https://pypi.python.org/pypi/python-redmine>`_ for more details.
    """

    try:
        # start creating/setting-up REDMINE project space
        update_setup_status_working(project_management)
        
        # create REDMINE project space
        settings = Settings.objects.all().get(user=user)
        project = project_management.project
        project_name = project.name
        project_identifier = project.slug
        project_description = project.description

        redmine_url = settings.redmine_url
        redmine_key = settings.redmine_key
        redmine = Redmine(redmine_url, key=redmine_key, version='2.3.3', requests={'verify': False})
        redmine_project = redmine.project.create(name=project_name, identifier=project_identifier, description=project_description)

        # done creating REDMINE project space
        project_management.url = urljoin(redmine_url, "projects/" + project_identifier)
        update_setup_status_done(project_management)

        return True

    except Exception as error:
        # failed to create REDMINE project - prompt for retry
        error_message =  "%s %s" % (str(error), type(error))
        LOGGER.error("REDMINE project space creation failed. (%s)" % error_message)
        update_setup_status_failed(project_management, error_message)
        return False

def project_setup_retry(project_id, setup_type, user):
    """
    Retries creating a specific project tool.

    :param project_id: Current project's id.
    :param setup_type: What tool to attempt a retry in creating.
    :param user: Current user logged in.

    :returns: ``True`` if successful, otherwise ``False``.

    It checks the ``setup_type`` and determine what *setup* function to use.

    ::

      setup_repository()
      setup_test_site()
      setup_jira_space()
      setup_redmine_space()

    and all these functions will return either ``True`` or ``False`` for its creation status.

    """
    # retry/create selected setup type for project
    project = Project.objects.all().get(pk=project_id)
    
    success = True

    if "repository" == setup_type:
        project_repository = ProjectRepository.objects.all().get(project=project)
        success = setup_repository(project_repository, user)
    elif "test-site" == setup_type:
        project_test_site = ProjectTestSite.objects.all().get(project=project)
        project_repository = ProjectRepository.objects.all().get(project=project)
        success = setup_test_site(project_test_site, project_repository, user)
    elif "jira" == setup_type:
        project_management = ProjectManagement.objects.all().get(project=project, pm_tool=ProjectManagement.JIRA)
        success = setup_jira_space(project_management)
    elif "redmine" == setup_type:
        project_management = ProjectManagement.objects.all().get(project=project, pm_tool=ProjectManagement.REDMINE)
        success =  setup_redmine_space(project_management, user)

    return success;

def update_setup_status(status_model, status, remarks=None):
    """General update of the status of a given PM tool.

    :param status_model: The tool passed to update its status.
    :param status: Current tool status.
    :param remarks: Remarks regarding tool status.

    """
    status_model.remarks = remarks
    status_model.status = status
    status_model.save()

def update_setup_status_new(status_model):
    """Sets the status of a given PM tool to ``NEW``.

    :param status_model: The tool passed to update its status.

    """
    update_setup_status(status_model, ProjectSetupStatus.NEW)

def update_setup_status_skip(status_model):
    """Sets the status of a given PM tool to ``SKIP``.

    :param status_model: The tool passed to update its status.

    """
    update_setup_status(status_model, ProjectSetupStatus.SKIP)

def update_setup_status_working(status_model):
    """Sets the status of a given PM tool to ``WORKING``.

    :param status_model: The tool passed to update its status.

    """
    update_setup_status(status_model, ProjectSetupStatus.WORKING)

def update_setup_status_failed(status_model, error_message=None):
    """Sets the status of a given PM tool to ``FAILED``.

    :param status_model: The tool passed to update its status.
    :param error_message: Error message that was fetched from its creation process.

    """
    update_setup_status(status_model, ProjectSetupStatus.FAILED, error_message)

def update_setup_status_done(status_model):
    """Sets the status of a given PM tool to ``DONE``.

    :param status_model: The tool passed to update its status.

    """
    update_setup_status(status_model, ProjectSetupStatus.DONE)

def create_NGINX_file():
    """
    Creates the necessary NGINX file needed to run the project to a test site.

    """
    current_directory = os.getcwd()
    conf_path = current_directory + "/auth_db/jumpstart_nginx.conf"
    shutil.copy (conf_path, current_directory)
