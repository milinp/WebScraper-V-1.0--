from upload.models import Document
from upload.forms import DocumentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from upload.forms import UserInputForm
import upload
import os
import boto
import re

location = ""

def home(request):
	global location
	userInput = UserInputForm

	if 'import' in request.POST:
		newdoc = Document(docfile = request.FILES['upload'])
		newdoc.save()
		location = newdoc.path()

		# creating S3 bucket connection
		conn = boto.connect_s3('AKIAIJZ56E33VC2GBG3Q', 'xfSWxuK9uGAsRwtwdJgIPBhiye0Z3ka5oRqRa8FD')
		bucket = conn.create_bucket('client1.bucket')
		k = Key(bucket)

		filename = str(request.FILES['upload'])
		filenameKey = re.sub('\.txt$', '', filename)

		print filenameKey
		
		k.key = filenameKey 
		k.set_contents_from_filename(location)
		return HttpResponseRedirect(reverse('upload.views.home'))
	else:
		form = DocumentForm() # An empty, unbound form

	if 'user_input' in request.POST:
		form = UserInputForm(request.POST)
		if form.is_valid():
			form.save()
			myfile = open(os.path.dirname(os.path.abspath(upload.__file__))+ "/media/Watchlists/userinput.txt", 'a')
			myfile.write(request.POST['keyword'] + "\n")
			myfile.close()

			location = os.path.dirname(os.path.abspath(upload.__file__))+ "/media/Watchlists/userinput.txt"

			conn = boto.connect_s3('AKIAIJZ56E33VC2GBG3Q', 'xfSWxuK9uGAsRwtwdJgIPBhiye0Z3ka5oRqRa8FD')
			bucket = conn.create_bucket('client1.bucket')
			k = Key(bucket)

			filenameKey = "userinput"

			print filenameKey
		
			k.key = filenameKey 
			k.set_contents_from_filename(location)
			return HttpResponseRedirect(reverse('upload.views.home'))
		else:
			form = UserInputForm()

	# Load documents for the list page
	documents = Document.objects.all()

	# Rendner list page with the documents and the form
	return render_to_response(
		'upload/parallax.html',
		{'documents': documents, 'form' : form, 'userInput' : userInput},
		context_instance = RequestContext(request)
	)

def logout(request):
	return logout_then_login(request)