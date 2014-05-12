# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectType'
        db.create_table(u'projects_projecttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'projects', ['ProjectType'])

        # Adding model 'ProjectTemplate'
        db.create_table(u'projects_projecttemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('repo_https', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('repo_ssh', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'projects', ['ProjectTemplate'])

        # Adding model 'ProjectRepository'
        db.create_table(u'projects_projectrepository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('repo_https', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('repo_ssh', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'projects', ['ProjectRepository'])

        # Adding model 'ProjectManagement'
        db.create_table(u'projects_projectmanagement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'projects', ['ProjectManagement'])

        # Adding model 'ProjectTestSite'
        db.create_table(u'projects_projecttestsite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'projects', ['ProjectTestSite'])

        # Adding model 'Project'
        db.create_table(u'projects_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('project_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectType'])),
            ('project_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectTemplate'])),
            ('project_repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectRepository'])),
            ('project_management', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectManagement'])),
            ('project_test_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectTestSite'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'projects', ['Project'])


    def backwards(self, orm):
        # Deleting model 'ProjectType'
        db.delete_table(u'projects_projecttype')

        # Deleting model 'ProjectTemplate'
        db.delete_table(u'projects_projecttemplate')

        # Deleting model 'ProjectRepository'
        db.delete_table(u'projects_projectrepository')

        # Deleting model 'ProjectManagement'
        db.delete_table(u'projects_projectmanagement')

        # Deleting model 'ProjectTestSite'
        db.delete_table(u'projects_projecttestsite')

        # Deleting model 'Project'
        db.delete_table(u'projects_project')


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project_management': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectManagement']"}),
            'project_repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectRepository']"}),
            'project_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectTemplate']"}),
            'project_test_site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectTestSite']"}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'projects.projectmanagement': {
            'Meta': {'object_name': 'ProjectManagement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'projects.projectrepository': {
            'Meta': {'object_name': 'ProjectRepository'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo_https': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'repo_ssh': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'})
        },
        u'projects.projecttemplate': {
            'Meta': {'object_name': 'ProjectTemplate'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'repo_https': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'repo_ssh': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'projects.projecttestsite': {
            'Meta': {'object_name': 'ProjectTestSite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'projects.projecttype': {
            'Meta': {'object_name': 'ProjectType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['projects']