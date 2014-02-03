PyEasyZip
=========

PyEasyZip is a small utility aimed at easing the automation of creating numerous .zip files.

For example, if you wanted to zip dozens of folders into separate archives, you'd usually need to manually
zip each folder. PyEasyZip automates the process, recursively zipping separate folders.

eg. If you had one folder
/home/user/Novel/Volume 1
and within that folder you had
/home/user/Novel/Volume 1/Chapter 01
/home/user/Novel/Volume 1/Chapter 02
...
/home/user/Novel/Volume 1/Chapter 30
you could tell PyEasyZip to recursively zip the directory '/home/user/Novel/Volume 1', thus creating
/home/user/Novel/Volume 1/Chapter 01.zip
/home/user/Novel/Volume 1/Chapter 02.zip
...
/home/user/Novel/Volume 1/Chapter 30.zip

The reason why you might wish to archive multiple different folders separately yet simultaneously varies.

eg. You may wish to archive thousands, even millions of files.
You could wrap them all into one archive, but in doing so you would create a single, potentially very large zip file.
Thereafter, you'd need to access or manipulate a very large zip file whenever you wish to access, modify or delete even one of the innumerable files within.
By recursively creating numerous zip files, each archive contains relevant, grouped files, as per the original directory structure. You can modify one archive without affecting any others, you could easily transfer an archive without moving a bunch of unnecessary data, etc.

-----------------------

Command line parameters

Commands can be separate or joined. eg. -o -t -a is the same as -ota.
Order doesn't matter either. -ota is the same as -ato.
What DOES matter is the position of the arguments in regards to folders to zip.
Running the command 'python ZipCLI.py -o /path/to/folder' is not the same as 'python ZipCLI.py /path/to/folder -o'.
CLI parameters only take effect if they come before a file path.

-o overwrite		If zip file exists, overwrite. If false, skip that directory.
-t top level only	If true, only zips the top directory. Doesn't recurse into subdirectories.
-a encompass all	-t switch must be used as well. Recurses into subdirectories and adds their contents to the top level archive.

Examples:

ex1
folder to zip: /home/user/novel/vol1
/home/user/novel/vol1.zip already exists

'python ZipCLI.py /home/user/novel/vol1' would not see that /home/user/novel/vol1.zip already exists and thus do nothing.
'python ZipCLI.py -o /home/user/novel/vol1' would create the zip file anew, whether it already exists or not.
'python ZipCLI.py /home/user/novel/vol1 -o' is the same as the first attempt; -o isn't specified until AFTER the file zipping has been attempted.

ex2
folder to zip: /home/user/novel/vol1
inner folders include:
-/home/user/novel/vol1/ch1
-/home/user/novel/vol1/ch2
-/home/user/novel/vol1/ch3
inner files include:
-/home/user/novel/vol1/ch1/page1
-/home/user/novel/vol1/ch2/page2
-/home/user/novel/vol1/ch3/page3

'python ZipCLI.py /home/user/novel/vol1' would create the archives /home/user/novel/vol1/ch1.zip, /home/user/novel/vol1/ch2.zip and /home/user/novel/vol1/ch3.zip
'python ZipCLI.py -a /home/user/novel/vol1' would do the same as the first attempt; -a is useless without -t
'python ZipCLI.py -t /home/user/novel/vol1' would only parse /home/user/novel/vol1, and since it only contains folders, not any actual files, no zip file would be created.
'python ZipCLI.py -ta /home/user/novel/vol1' would recurse into the subdirectories and use their contents as the top level archive's contents. As such, we'd end up with the archive /home/user/novel/vol1.zip containing page1, page2 and page3.