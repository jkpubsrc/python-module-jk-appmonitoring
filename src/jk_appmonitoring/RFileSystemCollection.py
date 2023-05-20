


import jk_typing
import jk_prettyprintobj

from .RFileSystem import RFileSystem
from .RDirectory import RDirectory






class RFileSystemCollection(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self):
		self.__fileSystems = {}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def filesystems(self) -> tuple:
		ret = sorted(self.__fileSystems.values(), key=lambda x: x.mountPoint)
		return tuple(ret)
	#

	@property
	def hasData(self) -> bool:
		if self.__fileSystems:
			for fs in self.__fileSystems:
				if not fs.hasData:
					return False
			return True
		else:
			return False
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"filesystems",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def clear(self):
		self.__fileSystems.clear()
	#

	@jk_typing.checkFunctionSignature()
	def registerDirectory(self, directory:RDirectory):
		assert isinstance(directory, RDirectory)
		if directory.mountPoint not in self.__fileSystems:
			raise Exception("Mount point not registered: " + directory.mountPoint)
		self.__fileSystems[directory.mountPoint]._registerDirectory(directory)
	#

	@jk_typing.checkFunctionSignature()
	def registerFileSystem(self, fs:RFileSystem):
		self.__fileSystems[fs.mountPoint] = fs
	#

	def hasMountPoint(self, mountPoint:str):
		return mountPoint in self.__fileSystems
	#

	def update(self):
		for fs in self.__fileSystems.values():
			fs.update()
	#

	def invalidate(self):
		for fs in self.__fileSystems.values():
			fs.invalidate()
	#

#










