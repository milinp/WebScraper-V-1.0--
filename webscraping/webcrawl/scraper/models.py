import os, re 
import scraper
from django.db import models
from django.db.models.base import ModelBase

# excuse the names
# model used for Pastebin entries
class DummyVisited(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	urlData = models.TextField()
	urlInfo = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = False)
	def __unicode__(self):
		return "URL: %s" % self.url

# model used for Pastie entries
class PastieEntries(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	urlData = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = False)
	def __unicode__(self):
		return "URL: %s" % self.url

# model used for upload functionality
class Document(models.Model):
	docfile = models.FileField(upload_to='Watchlists')
	def __unicode__(self):
		return self.docfile.name
	# Used to get the path of specific watchlist to pass on to the readfile.py matching process
	def path(self):
		m = re.search('<Document: (.*?)>', str(self.path))
		return os.path.dirname(os.path.abspath(scraper.__file__)) + "/media/" + str(m.group(1)) # MEDIA_ROOT + watchlist/name

# model used to figure out the most recent matches
class ModifiedWatchListDB(models.Model):
	matchedWord = models.CharField(primary_key = True, max_length = 255)
	modifiedTime = models.DateTimeField()

		
