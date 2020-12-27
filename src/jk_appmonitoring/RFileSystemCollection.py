


import time

import jk_typing
import jk_utils
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
	def fileSystems(self) -> tuple:
		ret = sorted(self.__fileSystems.values(), key=lambda x: x.mountPoint)
		return tuple(ret)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"fileSystems",
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

	def update(self):
		for fs in self.__fileSystems.values():
			fs.update()
	#

	def invalidate(self):
		for fs in self.__fileSystems.values():
			fs.invalidate()
	#

#










