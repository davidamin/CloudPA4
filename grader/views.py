from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Context, RequestContext, loader
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import JsonResponse

from django.utils import dateparse

from datetime import datetime

from django.conf import settings

import os
import json
import logging
import subprocess
import threading

from django.core.files.base import ContentFile

def index(request):
	return HttpResponse('<html><title> Cloud HW4 Grading Site </title><body>Submit your Walk.cc file. <form method="post" enctype="multipart/form-data" action="/test"><input type="file" name="code" /><input type="submit" name="submit" value="Upload" /></form></body></html>')

def test(request):
	file_content = ContentFile( request.FILES['code'].read() )
	fout = open('uploads/walk.cc', 'wb+')
	for chunk in file_content.chunks():
		fout.write(chunk)
	fout.close()
	results = ""
	try:
		subprocess.call("rm -f ./a.out", shell=True)
		retcode = subprocess.call("/usr/bin/g++ uploads/walk.cc", shell=True)
		if retcode:
			return HttpResponse("failed to compile walk.cc")
		subprocess.call("rm -f ./output", shell=True)
		retcode = subprocess.call("./test.sh", shell=True)
		results += str("Score: " + str(retcode) + " out of 2 correct.")
		results += "<br />"
		results += ("*************Original submission*************")
		with open('uploads/walk.cc','r') as fs:
			results += str(fs.read()) + "<br />"
		subprocess.call("rm -f uploads/walk.cc", shell=True)
	except:
		results = "Sorry, something went wrong. Try again later."
	return HttpResponse(results)
	
	
