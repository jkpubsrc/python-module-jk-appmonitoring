


import typing
import time
import os

import jk_utils
import jk_utils.weakref
import jk_typing
import jk_prettyprintobj

from .RDirectory import RDirectory
from .RDiskSpacePart import RDiskSpacePart






class RFileSystem(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	#
	# Constructor.
	#
	# @param		str name			A human readable, descriptive name for this file system.
	# @param		str mountPoint		The mout point of this file system.
	# @param		bool bWeakDirRefs	If <c>True</c> manage all directories as weak references (= default). That means: Registered directory objects
	#									that are dropped by some system component seize to exist and are then no longer considered automatically.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, name:str, mountPoint:str, devicePath:str = None, bWeakDirRefs:bool = True):
		self.__name = name
		self.__mountPointPath = mountPoint
		self.__devicePath = devicePath

		self.__directoriesList = None
		if not bWeakDirRefs:
			self.__directoriesList = []

		self.__directoriesWeakList = jk_utils.weakref.WeakValueList()

		self.__diskSpaceUsages = None
		self.__fsSizeTotal = -1
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def name(self) -> str:
		return self.__name
	#

	@property
	def devicePath(self) -> str:
		return self.__devicePath
	#

	@property
	def mountPoint(self) -> str:
		return self.__mountPointPath
	#

	@property
	def fsSizeTotal(self) -> typing.Union[int,None]:
		if self.__fsSizeTotal < 0:
			return None
		return self.__fsSizeTotal
	#

	@property
	def fsSizeUsed(self) -> typing.Union[int,None]:
		if self.__fsSizeTotal < 0:
			return None
		ret = 0
		for u in self.__diskSpaceUsages:
			if u.partType not in [ "free", "reserved" ]:
				ret += u.diskSpaceUsed
		return ret
	#

	@property
	def fsSizeUsedPercent(self) -> typing.Union[float,None]:
		if self.__fsSizeTotal < 0:
			return None

		nUsed = self.fsSizeUsed
		return nUsed / self.__fsSizeTotal * 100
	#

	@property
	def fsSizeUsedFraction(self) -> typing.Union[float,None]:
		if self.__fsSizeTotal < 0:
			return None

		nUsed = self.fsSizeUsed
		return nUsed / self.__fsSizeTotal
	#

	@property
	def usages(self) -> typing.Union[typing.Tuple[RDiskSpacePart],None]:
		if self.__fsSizeTotal < 0:
			return None
		return self.__diskSpaceUsages
	#

	@property
	def hasData(self) -> bool:
		return (self.fsSizeTotal > 0) and bool(self.__diskSpaceUsages)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"name",
			"mountPoint",
			"devicePath",
			"fsSizeTotal",
			"usages",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def _registerDirectory(self, directory:RDirectory):
		assert isinstance(directory, RDirectory)

		if self.__directoriesList is not None:
			self.__directoriesList.append(directory)

		self.__directoriesWeakList.append(directory)

		self.invalidate()
	#

	def invalidate(self):
		self.__diskSpaceUsages = None
		self.__fsSizeTotal = -1
	#

	def update(self, bForce:bool = False):
		statvfs = os.statvfs(self.__mountPointPath)
		fsSizeTotal = statvfs.f_frsize * statvfs.f_blocks		# Size of filesystem in bytes

		# ----

		diskSpaceUsages = [
			None		# will be filled in later
		]
		n = fsSizeTotal

		temp = []
		for directory in self.__directoriesWeakList.itemsAlive:
			directory.update(bForce=bForce)
			temp.append((directory, directory.diskSpaceUsed))

		for directory, u in temp:
			diskSpaceUsages.append(
				RDiskSpacePart(directory.name, directory.dirPath, u, fsSizeTotal, "usedDir")
			)
			n -= u

		# calculate and add reserved space

		statvfs = os.statvfs(self.__mountPointPath)
		fsSizeTotal = statvfs.f_frsize * statvfs.f_blocks		# Size of filesystem in bytes
		_fsFreeSystem = statvfs.f_frsize * statvfs.f_bfree		# Actual number of free bytes
		fsFreeUser = statvfs.f_frsize * statvfs.f_bavail		# Number of free bytes that ordinary users are allowed to use (excl. reserved space)
		fsReservedRoot = _fsFreeSystem - fsFreeUser

		diskSpacePart_reserved = RDiskSpacePart("Reserved", None, fsReservedRoot, fsSizeTotal, "reserved")
		n -= fsReservedRoot
		diskSpacePart_free = RDiskSpacePart("Free", None, fsFreeUser, fsSizeTotal, "free")
		n -= fsFreeUser

		diskSpaceUsages[0] = RDiskSpacePart("Other", None, n, fsSizeTotal, "usedOther")

		diskSpaceUsages.append(diskSpacePart_free)
		diskSpaceUsages.append(diskSpacePart_reserved)

		# ----

		self.__fsSizeTotal = fsSizeTotal
		self.__diskSpaceUsages = tuple(diskSpaceUsages)
	#

#










