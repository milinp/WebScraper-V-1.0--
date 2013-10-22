# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Visited'
        db.create_table(u'scraper_visited', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('urlData', self.gf('django.db.models.fields.TextField')()),
            ('urlInfo', self.gf('django.db.models.fields.TextField')()),
            ('modifiedTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'scraper', ['Visited'])

        # Adding model 'URLToVisit'
        db.create_table(u'scraper_urltovisit', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal(u'scraper', ['URLToVisit'])

        # Adding model 'DummyVisited'
        db.create_table(u'scraper_dummyvisited', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('urlData', self.gf('django.db.models.fields.TextField')()),
            ('urlInfo', self.gf('django.db.models.fields.TextField')()),
            ('modifiedTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'scraper', ['DummyVisited'])

        # Adding model 'Document'
        db.create_table(u'scraper_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'scraper', ['Document'])

        # Adding model 'ScrapeCheck'
        db.create_table(u'scraper_scrapecheck', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('urlData', self.gf('django.db.models.fields.TextField')()),
            ('urlPublishedTime', self.gf('django.db.models.fields.TextField')()),
            ('modifiedTime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'scraper', ['ScrapeCheck'])


    def backwards(self, orm):
        # Deleting model 'Visited'
        db.delete_table(u'scraper_visited')

        # Deleting model 'URLToVisit'
        db.delete_table(u'scraper_urltovisit')

        # Deleting model 'DummyVisited'
        db.delete_table(u'scraper_dummyvisited')

        # Deleting model 'Document'
        db.delete_table(u'scraper_document')

        # Deleting model 'ScrapeCheck'
        db.delete_table(u'scraper_scrapecheck')


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