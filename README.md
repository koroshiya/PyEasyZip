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