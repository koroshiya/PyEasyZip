#!/usr/bin/python2.7 -tt

import sys

if sys.version_info < (2, 7):
    print ("Must use python 2.7 or greater\n")
    sys.exit()
elif sys.version_info[0] > 2:
	print ("Incompatible with Python 3\n")
	sys.exit()

import zipfile
import os

class ZipCLI():

	def __init__(self, *args, **kwargs):
		self.overwrite    = False 
		self.topLevelOnly = False
		self.encompassAll = False
		self.verbose      = False
		self.incArchives  = False

		self.archiveFormats = ['zip','rar','tar','gz','xz','ar','bz2','7z','cbr','cbz']

	def printVerbose(self, *args):
		if self.verbose:
			argList = ''
			for arg in args:
				argList += arg + ' '
			print argList

	def processParam(self, arg):
		if arg[0] == '-':
			for param in arg[1:]:
				if param == 'o':
					self.overwrite = True
				elif param == 't':
					self.topLevelOnly = True
				elif param == 'a':
					self.encompassAll = True
				elif param == 'v':
					self.verbose = True
				elif param == 'z':
					self.incArchives = True
				else:
					pass
			return True
		else:
			return False

	def writeDirToZipRecursively(self, arg):
		fileList = []
		nameList = []
		for root, dirs, files in os.walk(arg):
			for f in files:
				fileList.append(root + '/' + f)
				nameList.append(f)
			for d in dirs:
				arrs = self.writeDirToZipRecursively(d)
				for f in arrs[0]:
					fileList.append(f)
				for n in arrs[1]:
					nameList.append(n)
		return [fileList, nameList]

	def zipDir(self, arg, nfiles):
		names = []
		files = []
		for f in nfiles:
			files.append(arg + '/' + f)
			names.append(f)
		self.zipDirDirectly(arg, files, names)

	def zipDirDirectly(self, arg, files, names):
		zipName = arg + '.zip';
		if os.path.isfile(zipName):
			if self.overwrite:
				if not os.access(os.path.dirname(arg), os.W_OK):
					self.printVerbose('Cannot delete file:', zipName)
					return
				else:
					os.remove(zipName)
			else:
				self.printVerbose(zipName, 'already exists')
				return
		zip = zipfile.ZipFile(zipName, 'w', compression=zipfile.ZIP_DEFLATED)
		for i in range(len(files)):
			if self.incArchives or not '.' in names[i] or '.' in names[i] and not names[i].split(".")[-1] in self.archiveFormats:
				zip.write(files[i], names[i])
			else:
				self.printVerbose('Skipping archive file',names[i])
		zip.close()
		self.printVerbose('Created zip file ' + os.path.basename(os.path.normpath(arg)) + '.zip')

	def processDir(self, arg):
		self.printVerbose('argument',arg)
		if not os.access(arg, os.R_OK):
			self.printVerbose('Cannot read from', arg)
		elif not os.access(os.path.dirname(arg), os.W_OK):
			self.printVerbose('Cannot write to', os.path.dirname(arg))
		else:
			for root, dirs, files in os.walk(arg):
				if self.topLevelOnly:
					if self.encompassAll:
						arrs = self.writeDirToZipRecursively(arg)
						self.zipDirDirectly(arg, arrs[0], arrs[1])
					else:
						self.zipDir(arg, files)
				else:
					for adir in dirs:
						self.processDir(arg + '/' + adir)
					self.zipDir(arg, files)
				return

if len(sys.argv) > 1:
	gui = ZipCLI()
	for arg in sys.argv:
		if gui.processParam(arg):
			pass
		elif os.path.isdir(arg):
			gui.processDir(arg)
else:
	print "No files specified"
