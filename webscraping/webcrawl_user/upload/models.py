import os, re
import upload
from django.db import models

class Document(models.Model):
	docfile = models.FileField(upload_to='Watchlists')
	def __unicode__(self):
		return self.docfile.name
	def path(self):
		m = re.search('<Document: (.*?)>', str(self.path))
		return os.path.dirname(os.path.abspath(upload.__file__))+ "/media/" + str(m.group(1))

class UserInput(models.Model):
	keyword = models.CharField(max_length = 50)
	def __unicode__(self):
		return "Keyword: %s" % self.keyword