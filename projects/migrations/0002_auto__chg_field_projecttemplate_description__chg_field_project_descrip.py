# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ProjectTemplate.description'
        db.alter_column(u'projects_projecttemplate', 'description', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Project.description'
        db.alter_column(u'projects_project', 'description', self.gf('django.db.models.fields.TextField')())

        # Changing field 'ProjectType.description'
        db.alter_column(u'projects_projecttype', 'description', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'ProjectTemplate.description'
        db.alter_column(u'projects_projecttemplate', 'description', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Project.description'
        db.alter_column(u'projects_project', 'description', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'ProjectType.description'
        db.alter_column(u'projects_projecttype', 'description', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
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
            'description': ('django.db.models.fields.TextField', [], {}),
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
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['projects']