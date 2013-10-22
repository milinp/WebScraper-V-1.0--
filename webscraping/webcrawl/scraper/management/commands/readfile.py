#!/usr/bin/python
import os
import MySQLdb
import sys
import scraper
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option

#for multipart mailing
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import dirname, join

# for SES and S3 storage : AWS
import boto.ses
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

#for screenshots
import re
import sys  
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

# Required for time zone conversion
from django.utils.timezone import utc
import datetime

# Database Models to refer the Database Tables
from scraper.models import DummyVisited, ModifiedWatchListDB


class Command(BaseCommand):
  def handle(self, *args, **options):
    main(args)


#Screenshot Class with its class methods
class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print 'saving', output_file
        image.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True

def main(args):
  print os.path.abspath(scraper.__file__)
  print "\t\t\t scheduling matching patterns start  \n\n\n"

  #creating an S3 Connection with the parameters as AWS key and AWS Secret
  conn = boto.connect_s3('AKIAIJZ56E33VC2GBG3Q', 'xfSWxuK9uGAsRwtwdJgIPBhiye0Z3ka5oRqRa8FD')

  #creating a unique Bucket for each client on the S3 Storage
  bucket = conn.get_bucket('client1.bucket')

  #Fetching all the Files in the s3 "client1.bucket" to make it generic to match with any number of watchlists
  for key in bucket.list():
    filename = key.name.encode('utf-8')
    print "File name is : "
    print filename
    key.get_contents_to_filename((dirname(__file__) +'\\'+ filename))
    watchListFile =  dirname(__file__) +'\\'+filename
    print "Printing watchlist"
    scanDatabaseForMatchList(watchListFile,filename)  

# This function scans the entire Table for a watchlist which contains watchWords
def scanDatabaseForMatchList(watchListFile, aFileName):
  listOfFiles = []

  #opens the watchlistFile reads all the words into the watchlist
  with open(watchListFile) as f:
      watchlist = f.readlines()
  db = MySQLdb.connect(host="interns-web.cwlx8eld8gjz.us-east-1.rds.amazonaws.com",user="interns",passwd="Dowjones1",db="url_info" )
  cursorPastebin = db.cursor()
  cursorPastie = db.cursor()
  fileSize = 0
  filePathName = ''
  i = 0

  #opens a file with name as "watchlist_name_01.txt" with a write mode in a specific project folder to log it.
  #so as to identify the attachment as per which watchlistFile it belonged to.
  #this file stores all the historical data
  print os.path.abspath(scraper.__file__)
  print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  "
  f = open(os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s_%d.txt' % (aFileName, i), 'w')
  for match in watchlist:
    try:
      matchingword = match.rstrip()
      # checks for the previous time stored in scraper_modifiedwatchlistdb whenever this watch word was sent or updated
      time = str(checkWatchListDB(matchingword))

      #gets the current time
      newModifiedTime = datetime.datetime.utcnow().replace(tzinfo = utc).strftime('%Y-%m-%d %H:%M:%S')
    

      #sql statement to check a match for the particular matching word between the previous stored time and the current time
      sqlPastebin = "SELECT * FROM scraper_dummyvisited WHERE urlData LIKE '%%%s%%' AND modifiedTime Between '%s' AND '%s';"  % (matchingword, time, newModifiedTime  )
      #print sqlPastebin
      keyword = matchingword
      #cursorPastebin.execute(sqlPastebin)
      
      #resultsPastebin = cursorPastebin.fetchall()
      resultsPastebin = "";
      sqlPastie = "SELECT * FROM scraper_pastieentries WHERE urlData LIKE '%%%s%%' AND modifiedTime Between '%s' AND '%s';"  % (matchingword, time, newModifiedTime  )
      print sqlPastie
      print "\n\n"
      cursorPastie.execute(sqlPastie)

      resultsPastie = cursorPastie.fetchall()
      #results = resultsPastie + resultsPastebin 
      results = resultsPastie
      if results:
        insertIntoWatchList(matchingword)
        latestUrl = results[-1][0]
        latestUrlData = results[-1][1]
      for row in results:
        # getting the filename and file path name
        fileName = "%s_%d.txt" %(aFileName, i)
        filePathName =  os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s' % (fileName)
        urlname = '%s-%d.png' % (matchingword , i)
        # stripping the escaping for the matches
        matches=re.findall(r'\'(.+?)\'',str(row))
        directoryName = os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s' % (fileName)
        tempFileSize = os.path.getsize(filePathName)  
        print "tempFileSize printing"
        print tempFileSize
        #checking the fileSize of the attachment which should be less than 20mb
        fileSize = float(tempFileSize)
        print fileSize
        if fileSize < 20000000:
          f = open(filePathName, 'a')
          f.write("\n\n\n-------------------------------------------------------------------------------------------------------\n\n")
          f.write("KEYWORD: " + matchingword + "\n\n\n") 
          f.write("Data Dump URL:  " + str(row[0]) + "\n\n\n")
          f.write("Content:  \n\n")
          f.write(str(row[1]) + "\n\n")
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
  db.close()

#This sends a mail using multi part request using SES.
def sendMail(filePath, fileName,matchingword,latestUrl,latestUrlData):
  msg = MIMEMultipart()
  msg['Subject'] = 'Dow Jones Cyber Security Risk Notification'
  msg['From'] = 'pranavkumar.patel@dowjones.com'
  addresses = ['pranav16@gmail.com', 'justineaitel@gmail.com']

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


# captures the screenshot for the url and stores it with the urlname.png
def takeScreenShots(url, matchingword):
  try:
    s = Screenshot() 
    print "\n!!!!!~~~~~~~~~~~~~`` URL  -  %s" % (url)

    screenshotname = os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s.png' % (matchingword)
    print "screenshotname name  = %s"  % (screenshotname)
    #screenshotname = matchingword + ".png"

    s.capture(url, screenshotname)
    return screenshotname
  except Exception as ex:
    print "Screenshot Exception in user code: " + str(ex)

#checks the database for existing watchword and return the previous modifiedTime
def checkWatchListDB(aWatchWord):
  if not ModifiedWatchListDB.objects.filter(matchedWord = aWatchWord).exists():
    return "00:00:00"
  else:
    modifiedWatchlistDB = ""
    modifiedWatchlistDB = ModifiedWatchListDB.objects.get(matchedWord = aWatchWord)  
    return modifiedWatchlistDB.modifiedTime.strftime('%Y-%m-%d %H:%M:%S')
 
 #insert or updates the database with the current modified Time
def insertIntoWatchList(aWatchWord):
  print "\n!!!!!~~~~~~~~~~~~aWatchWord  -  %s" % (aWatchWord)
  try:
    modifiedTime = datetime.datetime.utcnow().replace(tzinfo = utc)
    if ModifiedWatchListDB.objects.filter(matchedWord = aWatchWord).exists():
      print "\n!!!!!~~~~~~~~~~~~Updating  -  %s" % (aWatchWord)
      dummydata = ModifiedWatchListDB.objects.get(matchedWord = aWatchWord)
      dummydata.modifiedTime = modifiedTime
      dummydata.save()
      #ModifiedWatchListDB(matchedWord = aWatchWord, modifiedTime = modifiedTime).save()
    else:
      print "\n!!!!!~~~~~~~~~~~~inserting  -  %s" % (aWatchWord)
      ModifiedWatchListDB(matchedWord = aWatchWord, modifiedTime = modifiedTime).save()
  except Exception as ex:
      print "Inserting into the DB Exception in user code: " + str(ex)    