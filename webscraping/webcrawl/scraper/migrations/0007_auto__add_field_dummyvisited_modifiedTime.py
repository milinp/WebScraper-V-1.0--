# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DummyVisited.modifiedTime'
        db.add_column(u'scraper_dummyvisited', 'modifiedTime',
                      self.gf('django.db.models.fields.DateTimeField')(default=None),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DummyVisited.modifiedTime'
        db.delete_column(u'scraper_dummyvisited', 'modifiedTime')


    models = {
        u'scraper.document': {
            'Meta': {'object_name': 'Document'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'scraper.dummyvisited': {
            'Meta': {'object_name': 'DummyVisited'},
            'modifiedTime': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'urlData': ('django.db.models.fields.TextField', [], {}),
            'urlInfo': ('django.db.models.fields.TextField', [], {})
        },
        u'scraper.scrapecheck': {
            'Meta': {'object_name': 'ScrapeCheck'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifiedTime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'urlData': ('django.db.models.fields.TextField', [], {}),
            'urlPublishedTime': ('django.db.models.fields.TextField', [], {})
        },
        u'scraper.urltovisit': {
            'Meta': {'object_name': 'URLToVisit'},
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        u'scraper.visited': {
            'Meta': {'object_name': 'Visited'},
            'modifiedTime': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'urlData': ('django.db.models.fields.TextField', [], {}),
            'urlInfo': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['scraper']