#!/usr/bin/python2.7 -tt

import zipfile
import sys
import os

def processDir(arg):
	print arg
	#files = os.listdir(arg)
	for root, dirs, files in os.walk(arg):
		if len(dirs) > 0:
			for adir in dirs:
				processDir(arg + adir)
			return
		else:
			zip = zipfile.ZipFile(arg + '.zip', 'w', compression=zipfile.ZIP_DEFLATED)
			for f in files:
				zip.write(arg + '/' + f, f)
				#TODO: don't rearchive other archives
				#TODO: check if zip already exists
				#TODO: CLI args, such as overwrite?
			zip.close()
			print os.path.basename(os.path.normpath(arg)) + '.zip'

if len(sys.argv) > 1:
	for arg in sys.argv:
		if os.path.isdir(arg):
			processDir(arg)
else:
	print "No files specified"
