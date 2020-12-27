


import jk_sysinfo
import jk_prettyprintobj
import jk_utils

from .RProcess import RProcess
from .RProcessFilter import RProcessFilter









class RProcessList(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		super().__init__()
		self._rootProcesses = ()
		self._pidsToProcesses = {}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def rootProcesses(self) -> tuple:
		return self._rootProcesses
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"rootProcesses",
		]
	#

	"""
	def __calcSummary(self, key:str, parseFunc, jOut:dict):
		n = 0
		for p in self._pidsToProcesses.values():
			n += p[key]
		if parseFunc:
			jOut[key] = parseFunc(n)
		else:
			jOut[key] = n
	#
	"""

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def update(self):
		# prepare variables

		self._pidsToProcesses.clear()
		rootProcesses = []

		# retrieve data

		jProcessList = jk_sysinfo.get_ps(bAddVMemSize=False)

		# create a map of all process IDs

		for jProcess in jProcessList:
			p = RProcess(jProcess)
			self._pidsToProcesses[p.pid] = p

		# connect all processes with each other

		for p in self._pidsToProcesses.values():
			pp = self._pidsToProcesses.get(p.ppid)
			if pp is not None:
				pp._children.append(p)
				p.parent = pp

		# select all root processes

		for p in self._pidsToProcesses.values():
			if p.parent is None:
				rootProcesses.append(p)

		# finalize

		self._rootProcesses = tuple(rootProcesses)
	#

	#
	# Enrich all RProcess objects with more data.
	#
	def enrichWithMoreData(self):
		for p in self._pidsToProcesses.values():
			try:
				p.enrichWithMoreData()
			except Exception as ee:
				pass
	#

	def getAllPIDs(self) -> set:
		ret = set()
		for p in self._rootProcesses:
			p._getAllPIDsRecursively(ret)
		return ret
	#

	#
	# Extract a subset of the process tree based on the filter specified.
	#
	def filter(self, filter:RProcessFilter):
		assert isinstance(filter, RProcessFilter)

		ret = []

		currentCandidates = list(self._rootProcesses)
		nextCandidates = []
		while True:
			for p in currentCandidates:
				if filter.match(p):
					ret.append(p)
				else:
					nextCandidates.extend(p._children)
			if nextCandidates:
				currentCandidates = nextCandidates
				nextCandidates = []
			else:
				break
		
		pl = RProcessList()
		pl._rootProcesses = ret
		interestingPIDs = pl.getAllPIDs()
		for p in self._pidsToProcesses.values():
			if p.pid in interestingPIDs:
				pl._pidsToProcesses[p.pid] = p

		return pl
	#

	#
	# If not yet done enrich the processes with additional data and then calculate RSS memory and IO read/write summary.
	#
	def calcSummary(self, jOut:dict = None) -> dict:
		if jOut is None:
			jOut = {}
		else:
			assert isinstance(jOut, dict)

		for p in self._rootProcesses:
			p.calcSummary(jOut)

		return jOut
	#

#








