#!/usr/bin/python2.7 -tt

import sys

if sys.version_info < (2, 7):
    print ("Must use python 2.7 or greater\n")
    sys.exit()
elif sys.version_info[0] > 2:
	print ("Incompatible with Python 3\n")
	sys.exit()

try:
	import wx
	import wx.lib.scrolledpanel as scrolled
except ImportError:
	print ("You do not appear to have wxpython installed.\n")
	print ("Without wxpython, this program cannot run.\n")
	print ("You can download wxpython at: http://www.wxpython.org/download.php#stable \n")
	sys.exit()

import os
import ZipCLI

PARSE_ARGS = 650
FILE_CLOSE = 666
OPTIONS_OVERWRITE = 670
OPTIONS_TOP_LEVEL = 671
OPTIONS_ENCOMPASS_ALL = 672
OPTIONS_VERBOSE = 673
OPTIONS_INCLUDE_ARCHIVES = 674
INIT_TEXT = 'Drag files here to begin zipping'

class wxGUI(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(wxGUI, self).__init__(*args, **kwargs)

		dt = FileDrop(self)
		dt.SetFrame(self)
		self.SetDropTarget(dt)

		self.Bind(wx.EVT_CLOSE, self.Exit)

		self.SetTitle("wxPyEasyZip")

		self.ConstructMenu()
		self.textarea = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|wx.TE_RICH2, value=INIT_TEXT)
		self.textarea.SetDropTarget(dt)

		self.Show(True)

	def parseArgs(self, e):
		self.statusbar.SetStatusText('')
		if self.textarea.GetValue() == INIT_TEXT:
			self.statusbar.SetStatusText('Must enter at least one folder to zip')
			return
		data = self.textarea.GetValue().splitlines()

		cli = ZipCLI.ZipCLI()
		cli.overwrite = self.tOverwrite.IsChecked()
		cli.topLevelOnly = self.tTopLevel.IsChecked()
		cli.encompassAll = self.tEncompass.IsChecked()
		cli.verbose = self.tVerbose.IsChecked()
		cli.incArchives = self.tIncludeArchives.IsChecked()

		for i in reversed(xrange(0,len(data))):
			self.parseArg(data[i], cli)
			data.pop()
			self.textarea.SetValue('\n'.join(data))
		self.textarea.SetValue(INIT_TEXT)
		self.statusbar.SetStatusText('Finished')
	
	def parseArg(self, arg, cli):
		if os.path.isdir(arg):
			self.statusbar.SetStatusText('Parsing ' + arg)
			cli.processDir(arg)
		else:
			self.statusbar.SetStatusText(arg + ' is not a valid directory')

	def addArg(self, arg):
		if self.textarea.GetValue() == INIT_TEXT:
			self.textarea.SetValue('')
		else:
			self.textarea.AppendText('\n')
		self.textarea.AppendText(arg)

	def ConstructMenu(self):

		self.menubar = wx.MenuBar()
		menuFile = wx.Menu()
		menuParse = wx.Menu()
		menuOptions = wx.Menu()

		#menuFile.AppendSeparator()
		self.SetMenuItem(menuFile, FILE_CLOSE, '&Quit\tCtrl+Q', self.Exit)

		self.SetMenuItem(menuParse, PARSE_ARGS, '&Parse\tCtrl+P', self.parseArgs)

		self.tOverwrite = menuOptions.Append(OPTIONS_OVERWRITE, '&Overwrite\tCtrl+O', 
											'Overwrite zip file if it already exists', kind=wx.ITEM_CHECK)
		self.tTopLevel = menuOptions.Append(OPTIONS_TOP_LEVEL, '&Top Level Only\tCtrl+T', 
											'Only zip the specified directory, not its subdirectories', kind=wx.ITEM_CHECK)
		self.tEncompass = menuOptions.Append(OPTIONS_ENCOMPASS_ALL, '&Encompass All\tCtrl+A', 
											'Include files from subdirectories when only zipping the top level', kind=wx.ITEM_CHECK)
		self.tVerbose = menuOptions.Append(OPTIONS_VERBOSE, '&Verbose\tCtrl+V', 
											'Displays more verbose logging if started from the command line', kind=wx.ITEM_CHECK)
		self.tIncludeArchives = menuOptions.Append(OPTIONS_INCLUDE_ARCHIVES, '&Include Archives\tCtrl+Z', 
											'Zip archives found within the directory specified', kind=wx.ITEM_CHECK)

		self.menubar.Append(menuFile, '&File')
		self.menubar.Append(menuParse, '&Parse')
		self.menubar.Append(menuOptions, '&Options')

		self.statusbar = self.CreateStatusBar()
		self.SetMenuBar(self.menubar);

	def SetMenuItem(self, menu, idn, text, event):
		mItem = wx.MenuItem(menu, idn, text)
		menu.AppendItem(mItem)
		self.Bind(wx.EVT_MENU, event, id=idn)
		return mItem

	def Exit(self, e):
		wx.Exit()

class FileDrop(wx.FileDropTarget):
	def __init__(self, window):
		wx.FileDropTarget.__init__(self)
		self.window = window

	def SetFrame(self, frame):
		self.frame = frame;

	def OnDropFiles(self, x, y, filenames):
		for name in filenames:
			f.addArg(name)

JPy = wx.App(False)

options = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
#frame = wx.Frame(None, style=options)
f = wxGUI(wx.Frame(None, style=options));

JPy.MainLoop()