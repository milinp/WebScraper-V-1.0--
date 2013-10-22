from django.conf.urls import patterns, url
from scraper import views
from api import ArticleResource

article_resource = ArticleResource()

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^watchlist/$', views.watchlist, name='watchlist'),
	#url(r'^api/', include(article_resource.urls)),
)