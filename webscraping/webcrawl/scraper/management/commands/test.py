import urllib2, urlparse, sys, traceback, pdb, unicodedata, cookielib, time, threading, re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option
from django_cron import CronJobBase, Schedule
from django.core.management import call_command
from scraper.models import Cron_Visited, URLToVisit

# class MyCronJob(CronJobBase):
# 	RUN_EVERY_MINS = 5
# 	RUN_AT_TIMES = ['15:19']
# 	schedule = Schedule(run_at_times = RUN_AT_TIMES)
# 	code = 'scraper.my_cron_job'
# 	def do(self):
# 		# args = ['http://pastebin.com', '0']
# 		call_command('test', *args)

class Command(BaseCommand):
	def handle(self, *args, **options):
		# i = Cron_Visited.objects.get(id=1).id
		# i += 1
		Cron_Visited(url = "Banana").save()
