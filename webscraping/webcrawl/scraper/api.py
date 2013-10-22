from tastypie.resources import ModelResource
from tastypie.constants import ALL
from scraper.models import DummyVisited, PastieEntries



class ArticleResource(ModelResource):
	class Meta:
		queryset = PastieEntries.objects.all()
		resource_name = 'article'