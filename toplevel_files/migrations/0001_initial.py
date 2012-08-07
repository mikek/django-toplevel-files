# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TopLevelFileType'
        db.create_table('toplevel_files_toplevelfiletype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('file_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
        ))
        db.send_create_signal('toplevel_files', ['TopLevelFileType'])

        # Adding model 'TopLevelFile'
        db.create_table('toplevel_files_toplevelfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['toplevel_files.TopLevelFileType'], unique=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('mod_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('toplevel_files', ['TopLevelFile'])


    def backwards(self, orm):
        # Deleting model 'TopLevelFileType'
        db.delete_table('toplevel_files_toplevelfiletype')

        # Deleting model 'TopLevelFile'
        db.delete_table('toplevel_files_toplevelfile')


    models = {
        'toplevel_files.toplevelfile': {
            'Meta': {'ordering': "['-id']", 'object_name': 'TopLevelFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['toplevel_files.TopLevelFileType']", 'unique': 'True'})
        },
        'toplevel_files.toplevelfiletype': {
            'Meta': {'ordering': "['-id']", 'object_name': 'TopLevelFileType'},
            'file_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['toplevel_files']