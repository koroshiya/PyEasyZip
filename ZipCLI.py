#!/usr/bin/python2.7 -tt

import zipfile
import sys
import os

overwrite = False
topLevelOnly = False

def processParam(arg):
	if arg[0] == '-':
		for param in arg[1:]:
			print param
			if param == 'o':
				global overwrite
				overwrite = True
			elif param == 't':
				global topLevelOnly
				topLevelOnly = True
			else:
				pass
		return True
	else:
		return False

def zipDir(arg, dirs, files):
	zipName = arg + '.zip';
	if os.path.isfile(zipName):
		if overwrite:
			if not os.access(os.path.dirname(arg), os.W_OK):
				print 'Cannot delete file:', zipName
				return
			else:
				os.remove(zipName)
		else:
			print zipName, 'already exists'
			return
	zip = zipfile.ZipFile(zipName, 'w', compression=zipfile.ZIP_DEFLATED)
	for f in files:
		zip.write(arg + '/' + f, f)
		#TODO: don't rearchive other archives
	zip.close()
	print os.path.basename(os.path.normpath(arg)) + '.zip'

def processDir(arg):
	print arg
	#files = os.listdir(arg)
	for root, dirs, files in os.walk(arg):
		if topLevelOnly:
			zipDir(arg, dirs, files)
			return
		elif len(dirs) > 0:
			for adir in dirs:
				processDir(arg + '/' + adir)
			return
		else:
			if not os.access(arg, os.R_OK):
				print 'Cannot read from', arg
				continue
			elif not os.access(os.path.dirname(arg), os.W_OK):
				print 'Cannot write to', os.path.dirname(arg)
				continue
			zipDir(arg, dirs, files)

if len(sys.argv) > 1:
	for arg in sys.argv:
		if processParam(arg):
			pass
		elif os.path.isdir(arg):
			processDir(arg)
else:
	print "No files specified"
