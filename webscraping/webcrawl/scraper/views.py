import os
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.management import call_command # used to call script
from apscheduler.scheduler import Scheduler # used to schedule
import time, logging # used to schedule

from scraper.models import Document
from scraper.forms import DocumentForm

sched = Scheduler(standalone = True)
location = ""

def home(request):
	global sched

	# if pastebin button is pressed, invoke masterScrape to scrape pastebin archive
	# scheduler interval of 3 minutes
	if 'run_scraper_pastebin' in request.POST:
		logging.basicConfig()
		sched = Scheduler(standalone = True, coalesce = True)
		#coalesce is used to avoid APS scheduler missed job warning which in turn causes crashing
		args = ['http://pastebin.com/archive', '1', '180']
		call_command('masterScrape', *args)	
	
		def scrape_sched():
			call_command('masterScrape', *args)

		sched.add_interval_job(scrape_sched, seconds = 180, max_instances = 1000)
		sched.start()

	# if pastie button is pressed, invoke masterScrape to scrape pastie archive
	# scheduler interval of 10 minutes 
	if 'run_scraper_pastie' in request.POST:
		logging.basicConfig()
		sched = Scheduler(standalone = True, coalesce = True)
		args = ['http://pastie.org/pastes', '0', '60']
		call_command('masterScrape', *args)	
	
		def scrape_sched_pastie():
			call_command('masterScrape', *args)

		sched.add_interval_job(scrape_sched_pastie, seconds = 60, max_instances = 1000)
		sched.start()

	# sets flags to stop scrape function
	if 'stop_scraper' in request.POST:
		args = ['stop']
		call_command('masterScrape', *args)
		sched.shutdown(wait = False)

	return render(request, 'scraper/index2.0.html')

def watchlist(request):
#Handle file upload
	global location
	if 'import' in request.POST:
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()
			location = newdoc.path()
			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('scraper.views.watchlist'))
	else:
		form = DocumentForm() # An empty, unbound form

	if 'match' in request.POST:
		call_command('readfile', location)

		sched = Scheduler(standalone = True, coalesce = True)
		def match_sched():
			call_command('readfile', location)
		sched.add_interval_job(match_sched, seconds = 20, max_instances = 1000)
		sched.start()
		

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	return render_to_response(
		'scraper/index2.0.html',
		{'documents': documents, 'form' : form},
		context_instance = RequestContext(request)
	)
