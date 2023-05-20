

import typing

import jk_typing
import jk_prettyprintobj





#
# This class is an informational class. It provides information about backup volumes.
#
class RDiskSpacePart(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, name:str, dirPath:typing.Union[str,None], diskSpaceUsed:int, fsSizeTotal:int, partType:str):
		self.__name = name
		self.__dirPath = dirPath
		self.__nDiskSpaceUsed = diskSpaceUsed
		self.__nSizeTotal = fsSizeTotal
		self.__partType = partType
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# The type of this disk usage part
	#
	# @return	str		Returns the type of this part:
	#					* "free" if this reflects free disk space
	#					* "reserved" if this reflects disk space reserved for root
	#					* "usedDir" if this reflects disk space used based on specified directory trees
	#					* "usedOther" if this reflects disk space used by other files
	#
	@property
	def partType(self) -> str:
		return self.__partType
	#

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
	def diskSpaceUsedPercent(self) -> float:
		return self.__nDiskSpaceUsed / self.__nSizeTotal * 100
	#

	@property
	def diskSpaceUsedFraction(self) -> float:
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
			"partType",
			"dirPath",
			"diskSpaceUsed",
			"diskSpaceUsedPercent",
			"fsSizeTotal",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#










