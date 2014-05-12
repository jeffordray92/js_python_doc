"""
Fabric File to deploy django project
"""
import logging
import os

from fabric.api import *
from fabric.colors import green, red
from fabric.contrib import django
from contextlib import contextmanager

django.project('jumpstart')
from profiles.models import Settings



# globals
LOGGER = logging.getLogger("fabric")

settings = Settings.objects.first() 
user_home = os.path.expanduser('~')
path = user_home + "/" + str(settings.domain_path)
remote_user = settings.domain_user
remote_host = "%s@%s" % (remote_user,settings.domain_host)

def server():
    env.hosts = [remote_host]  # The Elastic IP to your server
    env.user =  remote_user    # your user on that system

@contextmanager
def errorhandling():
    try:
        yield
    except SystemExit as sys_error:
        LOGGER.error("Fabric execution Terminated. (return code: %s)" % sys_error)
        raise Exception("Fabric execution Terminated. (return code: %s)" % sys_error)

def clone(repo, proj_name):
    """ Clones project from project_repository to remote """
    with lcd("%s" % path):
        local("pwd")
        print(green("Initializing repository..."))
        local("git init")
        print(green("Cloning project from repository..."))
        local("git clone %s -b master" % repo)

def pull(repo, proj_name):
    """ Pulls master branch from project repository for redeployment """
    with lcd("%s" % path):
        local("pwd")
        with lcd("%s" % proj_name):
            print(green("Pulling master from GitHub..."))
            local("git pull origin master")

def venv(proj_name):
    """ Installs virtualenv and project requirements """
    with lcd("%s/%s" % (path, proj_name)):
        local("pwd")
        print(green("Installing virtualenv"))
        local("virtualenv env")
        with prefix("/bin/sh env/bin/activate"):
            local("env/bin/pip install -r requirements/base.txt")

def migrate(proj_name):
    """ Syncs, migrates and collects static files """
    with lcd("%s/%s/%s" % (path, proj_name, proj_name)):
        local("pwd")
        print(green("Syncing the database..."))
        local("python manage.py syncdb --no-initial-data --migrate --noinput")
        print(green("Migrating the database..."))
        local("python manage.py loaddata fixtures/initial_data.json")
        print(green("Collecting static files..."))
        local("python manage.py collectstatic --noinput")
        print(red("DONE!"))

def symlink(proj_name):
    """ Enables new project test site """
    sudo("ln -s %s/%s_nginx.conf /etc/nginx/sites-enabled/%s" % (path, proj_name, proj_name))

def restart():
    """ Restarts NGINX server"""
    sudo("/etc/init.d/nginx restart")

def deploy(repo, proj_name):
    """ Clones repository, install virtualenv and migrate apps """
    with errorhandling():
        clone(repo, proj_name)
        venv(proj_name)
        migrate(proj_name)
        #symlink(proj_name)
        #restart()

def redeploy(repo, proj_name):
    """ Pull updated codes from project repository and restart server"""
    with errorhandling():
        pull(repo, proj_name)
        #restart()

def rollback(proj_name):
    """ Remove project folder and symlink from remote """
    with lcd("%s" % path):
        local("rm -rf %s" % proj_name)
    #sudo("rm /etc/nginx/sites-enabled/%s" % proj_name)


def push(project_working_directory, project_name, repo_url):
    """ Push project files to project repository """
    with errorhandling():
        with lcd("%s" % project_working_directory):
            local("pwd")
            print(green("pushing project to repository..."))
            local("rm -r -f .git")
            local("git init")
            local("git add .")
            local("git commit -m ' %s - Initial Commit'" % project_name)
            local("git remote add origin %s" % repo_url)
            local("git remote set-url origin %s" % repo_url)
            local("git push origin master")            
            print(green( "done pushing project..."))
