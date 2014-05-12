# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Settings.repository_key'
        db.delete_column(u'profiles_settings', 'repository_key')

        # Adding field 'Settings.repository_username'
        db.add_column(u'profiles_settings', 'repository_username',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True),
                      keep_default=False)

        # Adding field 'Settings.repository_consumer_key'
        db.add_column(u'profiles_settings', 'repository_consumer_key',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True),
                      keep_default=False)

        # Adding field 'Settings.repository_consumer_secret'
        db.add_column(u'profiles_settings', 'repository_consumer_secret',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True),
                      keep_default=False)

        # Adding field 'Settings.repository_oauth_access_token'
        db.add_column(u'profiles_settings', 'repository_oauth_access_token',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True),
                      keep_default=False)

        # Adding field 'Settings.repository_oauth_access_token_secret'
        db.add_column(u'profiles_settings', 'repository_oauth_access_token_secret',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True),
                      keep_default=False)


        # Changing field 'Settings.redmine_url'
        db.alter_column(u'profiles_settings', 'redmine_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'Settings.redmine_key'
        db.alter_column(u'profiles_settings', 'redmine_key', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):
        # Adding field 'Settings.repository_key'
        db.add_column(u'profiles_settings', 'repository_key',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Deleting field 'Settings.repository_username'
        db.delete_column(u'profiles_settings', 'repository_username')

        # Deleting field 'Settings.repository_consumer_key'
        db.delete_column(u'profiles_settings', 'repository_consumer_key')

        # Deleting field 'Settings.repository_consumer_secret'
        db.delete_column(u'profiles_settings', 'repository_consumer_secret')

        # Deleting field 'Settings.repository_oauth_access_token'
        db.delete_column(u'profiles_settings', 'repository_oauth_access_token')

        # Deleting field 'Settings.repository_oauth_access_token_secret'
        db.delete_column(u'profiles_settings', 'repository_oauth_access_token_secret')


        # Changing field 'Settings.redmine_url'
        db.alter_column(u'profiles_settings', 'redmine_url', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Settings.redmine_key'
        db.alter_column(u'profiles_settings', 'redmine_key', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profiles.settings': {
            'Meta': {'object_name': 'Settings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jira_key': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'redmine_key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'redmine_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'repository_consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'repository_consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'repository_oauth_access_token': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'repository_oauth_access_token_secret': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'repository_username': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['profiles']