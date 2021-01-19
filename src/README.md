jk_appmonitoring
==========

Introduction
------------

This Python module contains components for analyzing the use of system resources by processes. It covers two use cases: a) monitoring other processes and b) monitoring one's own process.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-appmonitoring)
* [pypi.python.org](https://pypi.python.org/pypi/jk-appmonitoring)

Why this module?
----------------

Linux provides a lot of information about processes in the system via the `/proc/*` file system and other means. However to use this data easily a reasonable API is required. This module provides such an API. Some effort has been made to select appropriate information files and provide information about processes in a way that keeps the I/O and CPU load low.

Limitations of this module
--------------------------

This module is only usable on Linux.

This module can only provide information that is made available through regular system interfaces such as the `/proc/*` file system.

This module *only* provides information. This module is not ment to manage processes, it is only ment for retrieval of information about processes via a simple and well documented API. It therefore is ment not as a standalone application but as a building block within another application.

jk_appmonitoring and jk_sysinfo
----------------------

There is another module you should know about. It's named `jk_sysinfo`. While `jk_sysinfo` provides various information about the local machine and the operating system this module named `jk_appmonitoring` provides information about a single or a set of processes. `jk_sysinfo` is ment for system analysis and monitoring, `jk_appmonitoring` is ment for individual process analysis and monitoring.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_appmonitoring
```

Core API
----------------------

The core API provides the following functions:

* `dict get_proc_pid_io(int pid, *)` : Retrieve information about I/O of a process by parsing `/proc/<pid>/io`.
* `dict get_proc_pid_stat(int pid, *)` : Retrieve information about process memory usage and priority assignments by parsing `/proc/<pid>/stat`.
* `dict get_proc_pid_status(int pid, *)` : Retrieve information about process memory usage and priority assignments by parsing `/proc/<pid>/status`.

### `dict get_proc_pid_io(int pid, *)`

For a given process ID this function reads and parses `/proc/<pid>/io`. From this pseudo-file it will retrieve data and provide it using the following key-value-pairs:

| Key				| Data Type	| Description	|
| ---				| ---		| ---			|
| `io_read_bytes`	| `int`		| Count the number of bytes which this process causeed to be fetched from the storage layer. This is accurate for block-backed filesystems.	|
| `io_write_bytes`	| `int`		| Count the number of bytes which this process caused to be sent to the storage layer. (This should accurate for block-backed filesystems as well but there is no explicite information about that in the documentation for `/proc/<pid>/io`.)	|

### dict get_proc_pid_stat(int pid, *)`

For a given process ID this function reads and parses `/proc/<pid>/stat`. From this pseudo-file it will retrieve data and provide it using the following key-value-pairs:

| Key					| Data Type	| Description	|
| ---					| ---		| ---			|
| `cstime`				| `float`	| Amount of time that this process's waited-for children have been scheduled in **kernel mode**, measured in absolute number of seconds	|
| `cutime`				| `float`	| Amount of time that this process's waited-for children have been scheduled in **user mode**, measured in absolute number of seconds		|
| `io_delayacct_blkio`	| `float`	| Aggregated block I/O delays, measured in absolute number of seconds	|
| `nice`				| `int`		| The nice value (see setpriority(2)), a value in the range 19 (low priority) to -20 (high priority).		|
| `num_threads`			| `int`		| Number of threads in this process.			|
| `pgrp`				| `int`		| The process group ID of the process.					|
| `pid`					| `int`		| The process ID.					|
| `ppid`				| `int`		| The PID of the parent of this process.					|
| `mem_rss`				| `int`		| Resident Set Size: number of bytes the process has in real memory. This is just the bytes which count toward text, data, or stack space. This does not include bytes which have not been demand-loaded in, or which are swapped out.					|
| `stime`				| `float`	| Amount of time that this process has been scheduled in **kernel mode**, measured in absolute number of seconds					|
| `tty_nr`				| `int`		| The controlling terminal of the process. (The minor device number is contained in the combination of bits 31 to 20 and 7 to 0; the major device number is in bits 15 to 8.)	|
| `utime`				| `float`	| Amount of time that this process has been scheduled in **user mode**, measured in absolute number of seconds			|

### dict get_proc_pid_status(int pid, *)`

(TODO)






### Retrieving information about processes

(TODO)



Managing Disk Space Information
--------------------------------------------

If you want to display information about disk space the following set of classes can be used for that purpose:

* `RFileSystemCollection` : This manages all file systems available for analysis
* `RFileSystem` : This represents a file system available for analysis
* `RDirectory` : This represents a directory that is used by some part of an application

So the procedure is as follows:

* First instantiate a `RFileSystemCollection`,
* register all file systems `RFileSystemCollection` should check later, then
* register instances of `RDirectory` that represent a set of directories used by your application.
* Then invoke `update()` to retrieve more or less recent data (by respecting configurations for `RDirectory` to cache values for some time), and
* then retrieve the data from the `RFileSystem` objects via property `filesystems` from the `RFileSystemCollection`.

Here is a code example:

```python
fsCol = RFileSystemCollection()

# register a single file system - or main file system
fsCol.registerFileSystem(RFileSystem("Main", "/", bWeakDirRefs=False))

# now register various directories for demonstration purposes only
fsCol.registerDirectory(RDirectory("myuser-home", "/home/myuser", 60))
fsCol.registerDirectory(RDirectory("fileproc", "/srv/fileproc", 30))

# now update the file system usage data
fsCol.update()
```

The `RFileSystem` objects will now have generated disk usage information. You can access disk usage objects (represented by `RDiskSpacePart` objects) stored at these file system objects.

Here is a simple example how to do that:

```python
for fs in fsCol.filesystems:
	print(fs.name)
	for part in fs.usages:
		print("\t" + part.name + "\t" + str(part.diskSpaceUsedPercent))
```



Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



