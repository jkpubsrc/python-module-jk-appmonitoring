#!/usr/bin/python3


import typing
import os
import sys
import time

import jk_json
import jk_sysinfo
import jk_utils

from jk_appmonitoring import *






fsCol = RFileSystemCollection()
fsCol.registerFileSystem(RFileSystem("Main", "/", bWeakDirRefs=False))

fsCol.registerDirectory(RDirectory("woodoo-home", "/home/woodoo", 30))
fsCol.registerDirectory(RDirectory("thaniya", "/srv/thaniya", 30))
fsCol.registerDirectory(RDirectory("fileproc", "/srv/fileproc", 30))

fsCol.update()

fsCol.dump()



for fs in fsCol.fileSystems:
	print(fs.name)
	for part in fs.usages:
		print("\t" + part.name + "\t" + str(part.percentageOfTotal))













