PyEasyZip
=========

<ul>
<li><a href="#intro">Introduction</a></li>
<li><a href="#cliparams">Command line parameters</a></li>
<li><a href="#api">API Usage</a></li>
</ul>

<h2><span id="intro">Introduction</span></h2>

PyEasyZip is a small utility aimed at easing the automation of creating numerous .zip files.

For example, if you wanted to zip dozens of folders into separate archives, you'd usually need to manually
zip each folder. PyEasyZip automates the process, recursively zipping separate folders.

eg. If you had one folder<br>
-Volume 1<br>
and within that folder you had<br>
-Volume 1/Chapter 01<br>
-Volume 1/Chapter 02<br>
-Volume 1/Chapter ...<br>
-Volume 1/Chapter 30<br>
you could tell PyEasyZip to recursively zip the directory 'Volume 1', thus creating<br>
-Volume 1/Chapter 01.zip<br>
-Volume 1/Chapter 02.zip<br>
-Volume 1/Chapter ...<br>
-Volume 1/Chapter 30.zip<br>

The reason why you might wish to archive multiple different folders separately yet simultaneously varies.<br>
eg. You may wish to archive thousands, even millions of files, but don't want the archived data to be contained in a single, potentially very large zip file.<br>
You may wish to group similar data (eg. the different chapters of a book) to be sent to other people without sending a single, large file or a large amount of very small files.<br>

-----------------------

<h2 id="cliparams">Command line parameters</h2>

Commands can be separate or joined. eg. -o -t -a is the same as -ota.<br>
Order doesn't matter either. -ota is the same as -ato.<br>
What DOES matter is the position of the arguments in regards to folders to zip.<br>
Running the command 'python ZipCLI.py -o /path/to/folder' is not the same as 'python ZipCLI.py /path/to/folder -o'.<br>
CLI parameters only take effect if they come before a file path.<br>

-o overwrite		If zip file exists, overwrite. If false, skip that directory.<br>
-t top level only	If true, only zips the top directory. Doesn't recurse into subdirectories.<br>
-a encompass all	-t switch must be used as well. Recurses into subdirectories and adds their contents to the top level archive.<br>
-v verbose      If enabled, additional information is displayed in the command line.<br>
-z include archives If enabled, inner archives are added to the resulting zip. eg. Volume 1/Chapter 1.zip would be added to Volume 1.zip when created.

Examples:

ex1<br>
folder to zip: /home/user/novel/vol1<br>
/home/user/novel/vol1.zip already exists<br>

'python ZipCLI.py /home/user/novel/vol1' would not see that /home/user/novel/vol1.zip already exists and thus do nothing.<br>
'python ZipCLI.py -o /home/user/novel/vol1' would create the zip file anew, whether it already exists or not.<br>
'python ZipCLI.py /home/user/novel/vol1 -o' is the same as the first attempt; -o isn't specified until AFTER the file zipping has been attempted.<br>

ex2<br>
folder to zip: /home/user/novel/vol1<br>
inner folders include:<br>
-/home/user/novel/vol1/ch1<br>
-/home/user/novel/vol1/ch2<br>
-/home/user/novel/vol1/ch3<br>
inner files include:<br>
-/home/user/novel/vol1/ch1/page1<br>
-/home/user/novel/vol1/ch2/page2<br>
-/home/user/novel/vol1/ch3/page3<br>

'python ZipCLI.py /home/user/novel/vol1' would create the archives /home/user/novel/vol1/ch1.zip, /home/user/novel/vol1/ch2.zip and /home/user/novel/vol1/ch3.zip<br>
'python ZipCLI.py -a /home/user/novel/vol1' would do the same as the first attempt; -a is useless without -t<br>
'python ZipCLI.py -t /home/user/novel/vol1' would only parse /home/user/novel/vol1, and since it only contains folders, not any actual files, no zip file would be created.<br>
'python ZipCLI.py -ta /home/user/novel/vol1' would recurse into the subdirectories and use their contents as the top level archive's contents. As such, we'd end up with the archive /home/user/novel/vol1.zip containing page1, page2 and page3.<br>

------------------

<h2>API Usage</h2>

ZipCLI, the command line utility, is also a self-contained class within which you will find methods for parsing and zipping directories.<br>
Using ZipCLI from another class is quite straightforward. First, import ZipCLI.

import ZipCLI;

Then, create a ZipCLI object.

cli = ZipCLI.ZipCLI();

The CLI parameters can be set directly through the ZipCLI object.

cli.overwrite = True;<br>
cli.verbose = False;

Once you're satisfied with the settings, pass the ZipCLI object the directories to process.

cli.processDir('/home/User/Volume 1/');

And voila, we have created the /home/User/Volume 1.zip file.<br>
There are of course other methods contained within ZipCLI that can be used directly, but going through processDir and using the supplied parameters is the recommended procedure.
