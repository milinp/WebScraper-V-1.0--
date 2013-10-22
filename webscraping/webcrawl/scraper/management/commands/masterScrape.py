import urllib2
import urlparse
import cookielib
import time
import threading
import re
import sys
import pytz
import scraper
import dateutil.parser as dparser 
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from datetime import datetime
from pytz import timezone
from django.utils.timezone import utc
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import make_option
from scraper.models import DummyVisited, PastieEntries
# for SES and S3 storage : AWS
import boto.ses
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

#for multipart mailing
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import dirname, join

import os
from os.path import dirname, join

url = ""
wait = 0
url_key = ""
jar = cookielib.FileCookieJar("cookies")
isStop = False
urlArray = []
start_time = 0

class Command(BaseCommand):
	def handle(self, *args, **options):
		startTimer()
		if(args[0] == 'stop'):
			stopScraping()
		else:
			scraper(args)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, urlForScrape, url_key):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.urlForScrape = urlForScrape
        self.url_key = url_key
    def run(self):
    	if self.url_key == "pastebin.com":
        	startScraperPastebin(self.urlForScrape)
        if self.url_key == "pastie.org":
        	startScraperPastie(self.urlForScrape)

def scraper(args):
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  "	
	global urlArray
	global url
	global isStop
	global url_key
	isStop = False
	i = 0
	url = args[0]
	url_key = urlparse.urlsplit(url).netloc
	wait = float(args[1])
	try:
		urlArray = []		
		soup = openURL(url)
		if url_key == "pastie.org":
			addLinksPastie(soup)
			#getHistoricalDataPastie(soup)
			for i in range(0,8):
			 	soup = openURL(getPastieNextPage(soup))
			 	addLinksPastie(soup)
		if url_key == "pastebin.com":
			addLinksPastebin(soup)
		print "\n\n\n---------------------------------------Restarting----------------------------------------------------------------------------\n\n"
		print "Length of urlArray = %d\n\n\n" % (len(urlArray))
		file1 = open("urlArray.txt", "w");
		for url1 in urlArray:
  			file1.write("%s\n" % url1)	
		for urlForScrape in urlArray:
			status = getStatus()
			#print getTime()
			if status or getTime() > float(args[2]) - 2:
				#print("We killed it")
				print ""
			else: 
				i = i + 1
				threadName = "Thread number %d" % (i)
				thread = myThread(1, threadName, i, urlForScrape, url_key)
				time.sleep(wait)
				thread.start()
				thread.join()
				#urlArray.pop(0)
	except Exception as ex:
		print "Exception in user code: " + str(ex)

# invoked a thread to begin scraping a Pastebin page for information (specifically its date and contents)
# stores into database
def startScraperPastebin(urlForScrape):
	start_time = time.time()
	urlSoup = ""
	if not DummyVisited.objects.filter(url = urlForScrape).exists():
		print "new entry = %s\n\n" % (urlForScrape)
		print "opening url"
		urlSoup = openURL(urlForScrape)
		parsedText = scrapePastebin(urlSoup)
		modifiedTime = scrapeDatePastebin(urlSoup)
		match(urlForScrape,parsedText)
		DummyVisited(url = urlForScrape, urlData = parsedText, modifiedTime = modifiedTime).save()
	else:
		print "Repeated entry = %s\n" % (urlForScrape)

def match(urlForScrape, parsedText):
	conn = boto.connect_s3('AKIAIJZ56E33VC2GBG3Q', 'xfSWxuK9uGAsRwtwdJgIPBhiye0Z3ka5oRqRa8FD')
	#print "Inside Match"
  	#creating a unique Bucket for each client on the S3 Storage
  	bucket = conn.get_bucket('client1.bucket')

  	#Fetching all the Files in the s3 "client1.bucket" to make it generic to match with any number of watchlists
  	for key in bucket.list():
	    filename = key.name.encode('utf-8')
	    #print "File name is : "	
	    #print filename
	    key.get_contents_to_filename((dirname(__file__) +'\\'+ filename))
	    watchListFile =  dirname(__file__) +'\\'+filename
	    #print "Printing watchlist"
	    scanForMatchList(watchListFile,filename,urlForScrape,parsedText)

def scanForMatchList(watchListFile,filename,urlForScrape,parsedText):
  	listOfFiles = []
  	#print "Inside Scan"
  	#opens the watchlistFile reads all the words into the watchlist
 	with open(watchListFile) as f:
 		watchlist = f.readlines()
	fileSize = 0
	filePathName = ''
	i = 0

 	#opens a file with name as "watchlist_name_01.txt" with a write mode in a specific project folder to log it.
  	#so as to identify the attachment as per which watchlistFile it belonged to.
 	#this file stores all the historical data
 	#print os.path.abspath(os.path.dirname(__file__))
  	f = open(os.path.dirname(os.path.abspath(__file__)) + '\%s_%d.txt' % (filename, i), 'w')
  	for match in watchlist:
  		try:
  			matchingword = match.rstrip()
      		# checks for the previous time stored in scraper_modifiedwatchlistdb whenever this watch word was sent or updated
			checkMatch = matchingword in parsedText
			if checkMatch:
				latestUrl = urlForScrape
				latestUrlData = parsedText
			#for row in results:
				# getting the filename and file path name
				fileName = "%s_%d.txt" %(filename, i)
				filePathName =  os.path.dirname(os.path.abspath(__file__)) + '\%s' % (fileName)
				urlname = '%s-%d.png' % (matchingword , i)
				# stripping the escaping for the matches
				matches=re.findall(r'\'(.+?)\'',matchingword)
				directoryName = os.path.dirname(os.path.abspath(__file__)) + '\%s' % (fileName)
				tempFileSize = os.path.getsize(filePathName)  
				print matchingword
				#print tempFileSize
				#checking the fileSize of the attachment which should be less than 20mb
				fileSize = float(tempFileSize)
				print fileSize
				if fileSize < 20000000:
					f = open(filePathName, 'a')
					f.write("\n\n\n-------------------------------------------------------------------------------------------------------\n\n")
					f.write("KEYWORD: " + matchingword + "\n\n\n") 
					f.write("Data Dump URL:  " + urlForScrape + "\n\n\n")
					f.write("Content:  \n\n")
					f.write(parsedText + "\n\n")
					f.write("-------------------------------------------------------------------------------------------------------------\n\n")
					f.close()
					notificationWatchword = matchingword
					# once the matchingword has been found stored in the database.
				else:
					listOfFiles.add(fileName);
					i = i + 1
					# this fetches the last updated URL and the content stored in the URL
					#print "Printing the list of files \n\n\n\n"
					#print listOfFiles;
		except Exception as ex:
			print "Exception in Scan Database code: " + str(ex)

    # if match found it sends a mail through SES
	if filePathName:
		checkFileSize = float(os.path.getsize(filePathName))
		if checkFileSize > 100:
			sendMail(filePathName,fileName,notificationWatchword,latestUrl,latestUrlData)
	f.close()
	#	db.close()

def sendMail(filePath, fileName,matchingword,latestUrl,latestUrlData):
	print "Inside Match"
	msg = MIMEMultipart()
	subjectString = 'KeyWord: %s - Dow Jones Cyber Security Risk Notification' % (matchingword)
	msg['Subject'] = subjectString
	msg['From'] = 'pranavkumar.patel@dowjones.com'
	addresses = ['pranav.patel.1688@gmail.com', 'justineaitel@gmail.com']

	# what a recipient sees if they don't use an email reader
	msg.preamble = 'Multipart message.\n'
	part = MIMEText('**** Notification of keyword match ****\n\n This email serves as notification of possible security breach or potential targeting for a future incident.' 
	'The named data dump site is commonly used to share stolen data or information related to security breaches. Data related to your organization has been detected on this site.\n\n\n'
	'KEYWORD: %s' % matchingword + '\n\nData Dump URL:  %s' % latestUrl + '\n\nContent\n %s' % latestUrlData + '\n\n')
	msg.attach(part)
	part = MIMEApplication(open(filePath, 'rb').read())
	part.add_header('Content-Disposition', 'attachment', filename=fileName)
	msg.attach(part)

	# screenshotname = takeScreenShots(latestUrl, matchingword)
	# part = MIMEApplication(open(screenshotname, 'rb').read())
	# part.add_header('Content-Disposition', 'attachment', filename=matchingword+'.png')
	# msg.attach(part)
	# try:
	#   os.remove(screenshotname)
	# except OSError:
	#   pass
	# connect to SES
	try:
		connection =  boto.ses.connect_to_region('us-east-1',aws_access_key_id='AKIAIJZ56E33VC2GBG3Q', aws_secret_access_key='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')
		# and send the message to multiple email addresses
		result = connection.send_raw_email(msg.as_string()
		, source=msg['From']
		, destinations=addresses)
		print result
	except Exception as ex:
		print "Exception in user code: " + str(ex)


# invoked a thread to begin scraping a Pastie page for information (specifically its date and contents)
# stores into database
def startScraperPastie(urlForScrape):
	start_time = time.time()
	urlSoup = ""
	if not PastieEntries.objects.filter(url = urlForScrape).exists():
		print "new entry = %s\n\n" % (urlForScrape)
		urlSoup = openURL(urlForScrape)
		parsedText = scrapePastie(urlSoup)
		modifiedTime = scrapeDatePastie(urlSoup)
		
		if parsedText:
			print "\n\n ~~~~~~~~~~~~~~~~~~~~~~inside parsed Text"
			try:
				#print parsedText
				#print modifiedTime
				#print urlForScrape
				match(urlForScrape,parsedText)
				PastieEntries(url = urlForScrape, urlData = parsedText, modifiedTime = modifiedTime).save()
			except Exception as ex:
				print "Exception in user code: " + str(ex)
	else:
		print "Repeated entry  = %s\n" % (urlForScrape)

# syntaxy stuff to open the url with Cookies enabled
# takes in url (ex: http://bananaman.com)
# returns a BeautifulSoup object
def openURL(url):
	#time.sleep(wait)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	htmltext = BeautifulSoup(opener.open(url))
	return htmltext

# extract payload from Pastie site
# returns a string
def scrapePastie(soup):
	textBody = ""
	if soup.find("pre", attrs={"class" : "textmate-source"}):
		s = soup.find("pre", attrs={"class" : "textmate-source"})
		for f in s.findAll(text= True):
			textBody += f.encode("ascii", "ignore")
		return textBody

# extract payload from Pastebin site
# returns string
def scrapePastebin(soup):
	textBody = ""
	# check to see if div exists. It should because it's specific to pastebin.
	s = soup.find("textarea", attrs = {"id" : "paste_code"})
	textBody = s.text.encode("ascii", "ignore")
	return textBody

# extracts date of pastie post
# returns a datetime object (timezone = US/Eastern)
def scrapeDatePastie(soup):
	s = soup.findAll(title = True)
	if s:
		for time in s:
			dateString = time['title']
		pastieTime = dparser.parse(dateString,ignoretz= True)
		tz = pytz.timezone('GMT')	
		pastieTZ = tz.localize(pastieTime)
		pastieEST = pastieTZ.astimezone(pytz.timezone('US/Eastern'))
		pastieEST.strftime("%Y-%m-%d %H:%M:%S")
		return pastieEST
	else:
		return datetime(1993, 5, 21, 0, 0, 0, 0, None)

# extracts date of pastebin post
# returns a datetime object (timezone = US/Eastern)
def scrapeDatePastebin(soup):
	# check to see if div exists. It should because it's specific to pastebin.
	if soup.findAll("div", attrs = {"class" : "paste_box_info"}):
		# filter out the title attribute which holds the date
		for s in soup.findAll("span", title = True, style = True, text = True):
			dateString = s['title']
		# parses the pastebin time of post. pastebin time is default CDT (Central Date Time)
		pastebinTime = dparser.parse(dateString)
		tz = pytz.timezone('CST6CDT')
		pastebinTZ = tz.localize(pastebinTime)
		pastebinEST = pastebinTZ.astimezone(pytz.timezone('US/Eastern'))
		pastebinEST.strftime("%Y-%m-%d %H:%M:%S")
		return pastebinEST
	else:
		return datetime(1993, 5, 21, 0, 0, 0, 0, None)

# extracts all links on the archive/browse page of Pastie and stores into urlArray
def addLinksPastie(soup):
	s = soup.findAll("div", attrs={"class" : "pastePreview"})
	for section in s:
		linkTag = section.find("a")
		link = linkTag['href']
		urlArray.append(link)

# extracts all links on the archive/browse page of Pastebin and stores into urlArray
def addLinksPastebin(soup):
	maintable = soup.find("table", attrs = {"class" : "maintable"})
	if maintable:
		for a in maintable.findAll("a"):
			if "archive" not in a['href']:
		 		a['href'] = urlparse.urljoin("http://pastebin.com/", a['href'])
				urlArray.append(a['href'])

# extracts link to next page of Pastie archive (ex: http://pastie.org/pastes/y/2013/8/page/2)
# returns string
def getPastieNextPage(soup):
	if soup.find(text = "Next page").parent['href']:
		tag = soup.find(text = "Next page").parent['href']
		nextPage = urlparse.urljoin("http://pastie.org/", tag)
		return nextPage

# extracts all the historical data
def getHistoricalDataPastie(soup):
	if soup.findAll("div", attrs={"class" : "months"}):
		monthsURLSoup = soup.findAll("div", attrs={"class" : "months"})
		for eachMonth in monthsURLSoup:
			linkTag = eachMonth.find("a")
			print linkTag['href']
			link = urlparse.urljoin("http://pastie.org/", linkTag['href'])
			url1Array = getPastieNextPageRecursively(link)

def getPastieNextPageRecursively(nextURL):
	nextURLSoup = openURL(nextURL)
	if nextURLSoup.find(text = "Next page"):
		tag = nextURLSoup.find(text = "Next page").parent['href']
		nextPage = urlparse.urljoin("http://pastie.org/", tag)
		print "\n~~~~~~~~~ printing next Page ~~~~~~~~~~\n"
		print nextPage
		urlArray.append(nextURL)
		return getPastieNextPageRecursively(nextPage)
	else:
		return urlArray


# sets flags to stop scraping function
# invoked when Stop is pressed from Admin User Interface
def stopScraping():
	global isStop
	global urlArray
	print len(urlArray)
	#urlArray = []
	isStop = True

def startTimer():
	global start_time
	start_time = time.time()

def getTime():
	return time.time() - start_time

# check flag used for stopping
def getStatus()	:
	return isStop
