# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'upload_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'upload', ['Document'])

        # Adding model 'UserInput'
        db.create_table(u'upload_userinput', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'upload', ['UserInput'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'upload_document')

        # Deleting model 'UserInput'
        db.delete_table(u'upload_userinput')


    models = {
        u'upload.document': {
            'Meta': {'object_name': 'Document'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'upload.userinput': {
            'Meta': {'object_name': 'UserInput'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['upload']