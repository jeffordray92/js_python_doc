# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProjectManagement.project'
        db.add_column(u'projects_projectmanagement', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.Project']),
                      keep_default=False)

        # Adding field 'ProjectManagement.pm_tool'
        db.add_column(u'projects_projectmanagement', 'pm_tool',
                      self.gf('django.db.models.fields.CharField')(default='J', max_length=1),
                      keep_default=False)

        # Adding field 'ProjectRepository.project'
        db.add_column(u'projects_projectrepository', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.Project']),
                      keep_default=False)

        # Deleting field 'Project.project_management'
        db.delete_column(u'projects_project', 'project_management_id')

        # Deleting field 'Project.project_repository'
        db.delete_column(u'projects_project', 'project_repository_id')

        # Deleting field 'Project.project_test_site'
        db.delete_column(u'projects_project', 'project_test_site_id')

        # Adding field 'ProjectTestSite.project'
        db.add_column(u'projects_projecttestsite', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.Project']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProjectManagement.project'
        db.delete_column(u'projects_projectmanagement', 'project_id')

        # Deleting field 'ProjectManagement.pm_tool'
        db.delete_column(u'projects_projectmanagement', 'pm_tool')

        # Deleting field 'ProjectRepository.project'
        db.delete_column(u'projects_projectrepository', 'project_id')

        # Adding field 'Project.project_management'
        db.add_column(u'projects_project', 'project_management',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.ProjectManagement']),
                      keep_default=False)

        # Adding field 'Project.project_repository'
        db.add_column(u'projects_project', 'project_repository',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.ProjectRepository']),
                      keep_default=False)

        # Adding field 'Project.project_test_site'
        db.add_column(u'projects_project', 'project_test_site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.ProjectTestSite']),
                      keep_default=False)

        # Deleting field 'ProjectTestSite.project'
        db.delete_column(u'projects_projecttestsite', 'project_id')


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectTemplate']"}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'projects.projectmanagement': {
            'Meta': {'object_name': 'ProjectManagement'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'pm_tool': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'projects.projectrepository': {
            'Meta': {'object_name': 'ProjectRepository'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'repo_https': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'repo_ssh': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'})
        },
        u'projects.projecttemplate': {
            'Meta': {'object_name': 'ProjectTemplate'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectType']"}),
            'repo_https': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'repo_ssh': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'projects.projecttestsite': {
            'Meta': {'object_name': 'ProjectTestSite'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'projects.projecttype': {
            'Meta': {'object_name': 'ProjectType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['projects']