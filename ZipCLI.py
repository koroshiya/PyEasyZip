#!/usr/bin/python2.7 -tt

import zipfile
import sys
import os

overwrite    = False 
topLevelOnly = False
encompassAll = False
verbose      = False
incArchives  = False

archiveFormats = ['zip','rar','tar','gz','xz','ar','bz2','7z','cbr','cbz']

def printVerbose(*args):
	if verbose:
		argList = ''
		for arg in args:
			argList += arg + ' '
		print argList

def processParam(arg):
	if arg[0] == '-':
		for param in arg[1:]:
			if param == 'o':
				global overwrite
				overwrite = True
			elif param == 't':
				global topLevelOnly
				topLevelOnly = True
			elif param == 'a':
				global encompassAll
				encompassAll = True
			elif param == 'v':
				global verbose
				verbose = True
			elif param == 'z':
				global incArchives
				incArchives = True
			else:
				pass
		return True
	else:
		return False

def writeDirToZipRecursively(arg):
	fileList = []
	nameList = []
	for root, dirs, files in os.walk(arg):
		for f in files:
			fileList.append(root + '/' + f)
			nameList.append(f)
		for d in dirs:
			arrs = writeDirToZipRecursively(d)
			for f in arrs[0]:
				fileList.append(f)
			for n in arrs[1]:
				nameList.append(n)
	return [fileList, nameList]

def zipDir(arg, dirs, nfiles):
	names = []
	files = []
	for f in nfiles:
		files.append(arg + '/' + f)
		names.append(f)
	zipDirDirectly(arg, files, names)

def zipDirDirectly(arg, files, names):
	zipName = arg + '.zip';
	if os.path.isfile(zipName):
		if overwrite:
			if not os.access(os.path.dirname(arg), os.W_OK):
				printVerbose('Cannot delete file:', zipName)
				return
			else:
				os.remove(zipName)
		else:
			printVerbose(zipName, 'already exists')
			return
	zip = zipfile.ZipFile(zipName, 'w', compression=zipfile.ZIP_DEFLATED)
	for i in range(len(files)):
		if incArchives or not '.' in names[i] or '.' in names[i] and not names[i].split(".")[-1] in archiveFormats:
			zip.write(files[i], names[i])
		else:
			printVerbose('Skipping archive file',names[i])
	zip.close()
	printVerbose('Created zip file ' + os.path.basename(os.path.normpath(arg)) + '.zip')

def processDir(arg):
	printVerbose('argument',arg)
	for root, dirs, files in os.walk(arg):
		if topLevelOnly:
			if encompassAll:
				arrs = writeDirToZipRecursively(arg)
				zipDirDirectly(arg, arrs[0], arrs[1])
			else:
				zipDir(arg, dirs, files)
		elif len(dirs) > 0:
			for adir in dirs:
				processDir(arg + '/' + adir)
		else:
			if not os.access(arg, os.R_OK):
				printVerbose('Cannot read from', arg)
				return
			elif not os.access(os.path.dirname(arg), os.W_OK):
				printVerbose('Cannot write to', os.path.dirname(arg))
				return
			zipDir(arg, dirs, files)
		return

if len(sys.argv) > 1:
	for arg in sys.argv:
		if processParam(arg):
			pass
		elif os.path.isdir(arg):
			processDir(arg)
else:
	print "No files specified"
