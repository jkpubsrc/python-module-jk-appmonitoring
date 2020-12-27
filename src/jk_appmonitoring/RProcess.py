


import jk_prettyprintobj

from .get_proc_pid_information import *





class RProcess(dict, jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, data:dict):
		assert isinstance(data, dict)
		super().__init__(data)
		self.__pid = data["pid"]
		self.__ppid = data["ppid"]
		self._children = []
		self.parent = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def pid(self) -> int:
		return self.__pid
	#

	@property
	def ppid(self) -> int:
		return self.__ppid
	#

	@property
	def uid(self) -> int:
		return self["uid"]
	#

	@property
	def user(self) -> str:
		return self["user"]
	#

	@property
	def gid(self) -> int:
		return self["gid"]
	#

	@property
	def group(self) -> str:
		return self["group"]
	#

	@property
	def cmd(self) -> str:
		return self["cmd"]
	#

	@property
	def children(self) -> tuple:
		return tuple(self._children)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar("pid", self.__pid)
		ctx.dumpVar("user", self["user"])
		ctx.dumpVar("group", self["group"])
		ctx.dumpVar("cmd", self["cmd"])
		for key in sorted(self.keys()):
			if key not in [ "pid", "user", "cmd", "group" ]:
				ctx.dumpVar(key, self[key])
		ctx.dumpVar("children", self.children)
	#

	def _getAllPIDsRecursively(self, ret:set):
		currentProcesses = [ self ]
		nextProcesses = []
		while True:
			for jProcess in currentProcesses:
				ret.add(jProcess.pid)
				nextProcesses.extend(jProcess._children)
			if nextProcesses:
				currentProcesses = nextProcesses
				nextProcesses = []
			else:
				break
	#

	def __getAllProcesses(self, jList:list):
		jList.append(self)
		for p in self._children:
			p.__getAllProcesses(jList)
	#

	def __calcSummary(self, allProcesses:list, key:str, jOut:dict):
		n = jOut.get(key, 0)

		for p in allProcesses:
			n += p[key]

		jOut[key] = n
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self):
		return "RProcess<({}, '{}')>".format(self.__pid, self["cmd"])
	#

	def __repr__(self):
		return "RProcess<({}, '{}')>".format(self.__pid, self["cmd"])
	#

	def getAllPIDs(self) -> set:
		ret = set()
		self._getAllPIDsOfTree(ret)
		return ret
	#

	def enrichWithMoreData(self):
		for k, v in get_proc_pid_io(self.__pid).items():
			self[k] = v
		for k, v in get_proc_pid_stat(self.__pid).items():
			self[k] = v
	#

	#
	# If not yet done enrich the processes with additional data and then calculate RSS memory and IO read/write summary.
	#
	def calcSummary(self, jOut:dict = None) -> dict:
		if jOut is None:
			jOut = {}
		else:
			assert isinstance(jOut, dict)

		allProcesses = []
		self.__getAllProcesses(allProcesses)
		if not allProcesses:
			return jOut

		if "num_threads" not in self:
			self.enrichWithMoreData()

		self.__calcSummary(allProcesses, "num_threads", jOut)
		self.__calcSummary(allProcesses, "mem_rss", jOut)
		self.__calcSummary(allProcesses, "io_read_bytes", jOut)
		self.__calcSummary(allProcesses, "io_write_bytes", jOut)

		return jOut
	#

#








