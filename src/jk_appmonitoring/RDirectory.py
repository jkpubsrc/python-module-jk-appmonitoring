


import time
import typing

import jk_typing
import jk_utils
import jk_prettyprintobj





#
# This class is an informational class. It provides information about backup volumes.
#
class RDirectory(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, name:str, dirPath:str, cacheDurationSeconds:int):
		self.__name = name
		self.__cacheDurationSeconds = cacheDurationSeconds
		self.__dirPath = dirPath
		self.__mountPoint = jk_utils.fsutils.findMountPoint(self.__dirPath)
		assert self.__mountPoint

		self.__diskSpaceUsed = None
		self.__t = -1
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def name(self) -> str:
		return self.__name
	#

	@property
	def dirPath(self) -> str:
		return self.__dirPath
	#

	@property
	def mountPoint(self) -> str:
		return self.__mountPoint
	#

	@property
	def diskSpaceUsed(self) -> typing.Union[int,None]:
		return self.__diskSpaceUsed
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"name",
			"dirPath",
			"mountPoint",
			"diskSpaceUsed",
		]
	#

	def __doUpdate(self) -> int:
		self.__diskSpaceUsed = None
		self.__t = -1

		self.__t = time.time()
		self.__diskSpaceUsed = jk_utils.fsutils.getFolderSize(self.__dirPath, mode="block")
		return self.__diskSpaceUsed
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def update(self, bForce:bool = False) -> int:
		if (self.__diskSpaceUsed is None) or (self.__t + self.__cacheDurationSeconds >= time.time()) or bForce:
			self.__doUpdate()
		return self.__diskSpaceUsed
	#

	def invalidate(self):
		self.__diskSpaceUsed = None
		self.__t = -1
	#

#










