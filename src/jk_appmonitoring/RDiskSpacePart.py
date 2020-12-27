

import typing
import time

import jk_typing
import jk_utils
import jk_prettyprintobj





#
# This class is an informational class. It provides information about backup volumes.
#
class RDiskSpacePart(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, name:str, dirPath:typing.Union[str,None], diskSpaceUsed:int, fsSizeTotal:int):
		self.__name = name
		self.__dirPath = dirPath
		self.__nDiskSpaceUsed = diskSpaceUsed
		self.__nSizeTotal = fsSizeTotal
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
	def diskSpaceUsed(self) -> int:
		return self.__nDiskSpaceUsed
	#

	@property
	def percentageOfTotal(self) -> float:
		return self.__nDiskSpaceUsed / self.__nSizeTotal * 100
	#

	@property
	def fragmentOfTotal(self) -> float:
		return self.__nDiskSpaceUsed / self.__nSizeTotal
	#

	@property
	def fsSizeTotal(self) -> int:
		if self.__nSizeTotal < 0:
			self.update()
		return self.__nSizeTotal
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"name",
			"dirPath",
			"diskSpaceUsed",
			"percentageOfTotal",
			"fsSizeTotal",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#










