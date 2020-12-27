

import os
import typing
import resource

import jk_sysinfo
import jk_cmdoutputparsinghelper
import jk_json
import jk_utils





# see: https://stackoverflow.com/questions/4189123/python-how-to-get-number-of-mili-seconds-per-jiffy
# see: https://stackoverflow.com/questions/19919881/sysconf-sc-clk-tck-what-does-it-return
_CLKTCK_DUR = 1 / os.sysconf(os.sysconf_names["SC_CLK_TCK"])

_PAGESIZE = resource.getpagesize()
_PAGESIZE_KB = _PAGESIZE / 1024






_LINE_PARSER = jk_cmdoutputparsinghelper.LineParser_ParseAtFirstDelimiter()

#_VALUE_PARSER_BYTES = jk_utils.AmountOfBytes.parseFromStr
_VALUE_PARSER_BYTES = jk_cmdoutputparsinghelper.ValueParser_ByteWithUnit.parse


def _parseTabSeparatedIntList(s:str):
	return [ int(x) for x in s.split("\t") ]
#

def _parseSpaceSeparatedIntList(s:str):
	return [ int(x) for x in s.split(" ") ]
#


_VALUE_PARSERS_STATUS = {
	"VmData": _VALUE_PARSER_BYTES,
	"VmExe": _VALUE_PARSER_BYTES,
	"VmHWM": _VALUE_PARSER_BYTES,
	"VmLck": _VALUE_PARSER_BYTES,
	"VmLib": _VALUE_PARSER_BYTES,
	"VmPMD": _VALUE_PARSER_BYTES,
	"VmPTE": _VALUE_PARSER_BYTES,
	"VmPeak": _VALUE_PARSER_BYTES,
	"VmPin": _VALUE_PARSER_BYTES,
	"VmRSS": _VALUE_PARSER_BYTES,
	"VmSize": _VALUE_PARSER_BYTES,
	"VmStk": _VALUE_PARSER_BYTES,
	"VmSwap": _VALUE_PARSER_BYTES,
	"FDSize": int,
	"HugetlbPages": _VALUE_PARSER_BYTES,
	"NSpgid": int,
	"NSpid": int,
	"NSsid": int,
	"NStgid": int,
	"Ngid": int,
	"PPid": int,
	"Pid": int,
	"Seccomp": int,
	"Tgid": int,
	"Threads": int,
	"TracerPid": int,
	"nonvoluntary_ctxt_switches": int,
	"voluntary_ctxt_switches": int,
	"Gid": _parseTabSeparatedIntList,
	"Groups": _parseSpaceSeparatedIntList,
	"Uid": _parseTabSeparatedIntList,
}






#
# Returns something like this:
#
# {
# 	"CapAmb": "0000000000000000",
# 	"CapBnd": "0000003fffffffff",
# 	"CapEff": "0000000000000000",
# 	"CapInh": "0000000000000000",
# 	"CapPrm": "0000000000000000",
# 	"Cpus_allowed": "f",
# 	"Cpus_allowed_list": "0-3",
# 	"FDSize": 256,
# 	"Gid": [ 1000, 1000, 1000, 1000 ],
# 	"Groups": [ 4, 20, 24, 27, 30, 46, 113, 129, 138, 1000, 1006, 2004 ],
# 	"HugetlbPages": 0,
# 	"Mems_allowed": "00000000,00000001",
# 	"Mems_allowed_list": "0",
# 	"NSpgid": 11711,
# 	"NSpid": 11711,
# 	"NSsid": 1308,
# 	"NStgid": 11711,
# 	"Name": "test.py",
# 	"Ngid": 0,
# 	"PPid": 1308,
# 	"Pid": 11711,
# 	"Seccomp": 0,
# 	"ShdPnd": "0000000000000000",
# 	"SigBlk": "0000000000000000",
# 	"SigCgt": "0000000180000002",
# 	"SigIgn": "0000000001001000",
# 	"SigPnd": "0000000000000000",
# 	"SigQ": "1/124323",
# 	"Speculation_Store_Bypass": "thread vulnerable",
# 	"State": "R (running)",
# 	"Tgid": 11711,
# 	"Threads": 1,
# 	"TracerPid": 0,
# 	"Uid": [ 1000, 1000, 1000, 1000 ],
# 	"VmData": 23859200,
# 	"VmExe": 3833856,
# 	"VmHWM": 36483072,
# 	"VmLck": 0,
# 	"VmLib": 11259904,
# 	"VmPMD": 12288,
# 	"VmPTE": 233472,
# 	"VmPeak": 110043136,
# 	"VmPin": 0,
# 	"VmRSS": 36483072,
# 	"VmSize": 110039040,
# 	"VmStk": 135168,
# 	"VmSwap": 0,
# 	"nonvoluntary_ctxt_switches": 4,
# 	"voluntary_ctxt_switches": 12
# }
#
def get_proc_pid_status(pid:int, c = None) -> dict:
	assert isinstance(pid, int)
	assert pid > 0

	stdout, stderr, exitcode = jk_sysinfo.run(c, "cat /proc/" + str(pid) + "/status")

	stdoutLines = stdout.split("\n")

	ret = _LINE_PARSER.parseLinesReturnDict(stdoutLines, valueParserMap=_VALUE_PARSERS_STATUS)
	return ret
#




# see: "man proc"
_VALUE_SPECS_STAT = (
#	POS		MAN PAGE KEY NAME			KEY NAME TO USE		TYPE	FACTOR
	(	0,	"pid",						"pid",					int,	1			),	# The process ID.
	#		program
	(	1,	"state",					"state",				str,	None		),	# One of the following characters, indicating process state: R, S, D, Z, T, t, W, X, x, K, W, P
	(	2,	"ppid",						"ppid",					int,	1			),	# The PID of the parent of this process.
	(	3,	"pgrp",						"pgrp",					int,	1			),	# The process group ID of the process.
	#(	4,	"session",					"session",				int,	1			),	# The session ID of the process.
	(	5,	"tty_nr",					"tty_nr",				int,	1			),	# The controlling terminal of the process. (The minor device number is contained in the combination of bits 31 to 20 and 7 to 0; the major device number is in bits 15 to 8.)
	#(	6,	"tpgid",					"tpgid",				int,	1			),	# The ID of the foreground process group of the controlling terminal of the process.
	#(	7,	"flags",					"flags",				int,	1			),	# The kernel flags word of the process. For bit meanings, see the PF_* defines in the Linux kernel source file include/linux/sched.h. Details depend on the kernel version.
	#(	8,	"minflt",					"minflt",				int,	1			),	# The number of minor faults the process has made which have not required loading a memory page from disk.
	#(	9,	"cminflt",					"cminflt",				int,	1			),	# The number of minor faults that the process's waited-for children have made.
	#(	10,	"majflt",					"majflt",				int,	1			),	# The number of major faults the process has made which have required loading a memory page from disk.
	#(	11,	"cmajflt",					"cmajflt",				int,	1			),	# The number of major faults that the process's waited-for children have made.
	(	12,	"utime",					"utime",				int,	_CLKTCK_DUR	),	# Amount of time that this process has been scheduled in user mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)). This includes guest time, guest_time (time spent running a virtual CPU, see below), so that applications that are not aware of the guest time field do not lose that time from their calculations.
	(	13,	"stime",					"stime",				int,	_CLKTCK_DUR	),	# Amount of time that this process has been scheduled in kernel mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).
	(	14,	"cutime",					"cutime",				int,	_CLKTCK_DUR	),	# Amount of time that this process's waited-for children have been scheduled in user mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)). (See also times(2).) This includes guest time, cguest_time (time spent running a virtual CPU, see below).
	(	15,	"cstime",					"cstime",				int,	_CLKTCK_DUR	),	# Amount of time that this process's waited-for children have been scheduled in kernel mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).	(	,	"priority",				int,	1		),	# For processes running a real-time scheduling policy (policy below; see sched_setscheduler(2)), this is the negated scheduling priority, minus one; that is, a number in the range -2 to -100, corresponding to real- time priorities 1 to 99. For processes running under a non-real-time scheduling policy, this is the raw nice value (setpriority(2)) as represented in the kernel. The kernel stores nice values as numbers in the range 0 (high) to 39 (low), corresponding to the user-visible nice range of -20 to 19.
	#(	16,	"priority",					"priority",				int,	1			),	# For processes running a real-time scheduling policy (policy below; see sched_setscheduler(2)), this is the negated scheduling priority, minus one; that is, a number in the range -2 to -100, corresponding to realtime priorities 1 to 99. For processes running under a non-real-time scheduling policy, this is the raw nice value (setpriority(2)) as represented in the kernel. The kernel stores nice values as numbers in the range 0 (high) to 39 (low), corresponding to the user-visible nice range of -20 to 19.
	(	17,	"nice",						"nice",					int,	1			),	# The nice value (see setpriority(2)), a value in the range 19 (low priority) to -20 (high priority).
	(	18,	"num_threads",				"num_threads",			int,	1			),	# Number of threads in this process (since Linux 2.6).
	#(	19,	"itrealvalue",				"itrealvalue",			int,	1			),	# obsolete; The time in jiffies before the next SIGALRM is sent to the process due to an interval timer. Since kernel 2.6.17, this field is no longer maintained, and is hard coded as 0.
	#(	20,	"starttime",				"starttime",			int,	_CLKTCK_DUR	),	# The time the process started after system boot. In kernels before Linux 2.6, this value was expressed in jiffies. Since Linux 2.6, the value is expressed in clock ticks (divide by sysconf(_SC_CLK_TCK)).
	#(	21,	"vsize",					"mem_vsize",			int,	1			),	# Virtual memory size in bytes.
	(	22,	"rss",						"mem_rss",				int,	_PAGESIZE	),	# Resident Set Size: number of pages the process has in real memory. This is just the pages which count toward text, data, or stack space. This does not include pages which have not been demand-loaded in, or which are swapped out.
	#(	23,	"rsslim",					"mem_rsslim",			int,	_PAGESIZE	),	# Current soft limit in bytes on the rss of the process; see the description of RLIMIT_RSS in getrlimit(2).
	#(	24,	"startcode",				"startcode",			int,	1			),	# The address above which program text can run.
	#(	25,	"endcode",					"endcode",				int,	1			),	# The address below which program text can run.
	#(	26,	"startstack",				"startstack",			int,	1			),	# The address of the start (i.e., bottom) of the stack.
	#(	27,	"kstkesp",					"kstkesp",				int,	1			),	# The current value of ESP (stack pointer), as found in the kernel stack page for the process.
	#(	28,	"kstkeip",					"kstkeip",				int,	1			),	# The current EIP (instruction pointer).
	#(	29,	"signal",					"signal",				int,	1			),	# obsolete; use /proc/[pid]/status instead.
	#(	30,	"blocked",					"blocked",				int,	1			),	# obsolete; use /proc/[pid]/status instead.
	#(	31,	"sigignore",				"sigignore",			int,	1			),	# obsolete; use /proc/[pid]/status instead.
	#(	32,	"sigcatch",					"sigcatch",				int,	1			),	# obsolete; use /proc/[pid]/status instead.
	#(	33,	"wchan",					"wchan",				int,	1			),	# This is the "channel" in which the process is waiting. It is the address of a location in the kernel where the process is sleeping. The corresponding symbolic name can be found in /proc/[pid]/wchan.
	#(	34,	"nswap",					"nswap",				int,	1			),	# obsolete; Number of pages swapped (not maintained).
	#(	35,	"cnswap",					"cnswap",				int,	1			),	# obsolete; Cumulative nswap for child processes (not maintained).
	#(	36,	"exit_signal",				"exit_signal",			int,	1			),	# Signal to be sent to parent when process dies.
	#(	37,	"processor",				"processor",			int,	1			),	# CPU number last executed on.
	#(	38,	"rt_priority",				"rt_priority",			int,	1			),	# Real-time scheduling priority, a number in the range 1 to 99 for processes scheduled under a real-time policy, or 0, for non-real-time processes (see sched_setscheduler(2)).
	#(	39,	"policy",					"policy",				int,	1			),	# Scheduling policy (see sched_setscheduler(2)). Decode using the SCHED_* constants in linux/sched.h.
	(	40,	"delayacct_blkio_ticks",	"io_delayacct_blkio",	int,	_CLKTCK_DUR	),	# Aggregated block I/O delays, measured in clock ticks (centiseconds).
	#(	41,	"guest_time",				"guest_time",			int,	_CLKTCK_DUR	),	# Guest time of the process (time spent running a virtual CPU for a guest operating system), measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).
	#(	42,	"cguest_time",				"cguest_time",			int,	_CLKTCK_DUR	),	# Guest time of the process's children, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).
	#(	43,	"start_data",				"start_data",			int,	1			),	# Address above which program initialized and uninitialized (BSS) data are placed.
	#(	44,	"end_data",					"end_data",				int,	1			),	# Address below which program initialized and uninitialized (BSS) data are placed.
	#(	45,	"start_brk",				"start_brk",			int,	1			),	# Address above which program heap can be expanded with brk(2).
	#(	46,	"arg_start",				"arg_start",			int,	1			),	# Address above which program command-line arguments (argv) are placed.
	#(	47,	"arg_end",					"arg_end",				int,	1			),	# Address below program command-line arguments (argv) are placed.
	#(	48,	"env_start",				"env_start",			int,	1			),	# Address above which program environment is placed.
	#(	49,	"env_end",					"env_end",				int,	1			),	# Address below which program environment is placed.
	#(	50,	"exit_code",				"exit_code",			int,	1			),	# The thread's exit status in the form reported by waitpid(2).
)



#
# Returns something like this:
#
# {
# 	"cstime": 0.0,				# Amount of time that this process's waited-for children have been scheduled in kernel mode, measured in absolute number of seconds
# 	"cutime": 0.0,				# Amount of time that this process's waited-for children have been scheduled in user mode, measured in absolute number of seconds
#	"delayacct_blkio": 0.0,		# Aggregated block I/O delays, measured in absolute number of seconds
# 	"nice": 0,					# The nice value (see setpriority(2)), a value in the range 19 (low priority) to -20 (high priority).
# 	"num_threads": 1,			# Number of threads in this process.
# 	"pgrp": 1910,				# The process group ID of the process.
# 	"pid": 1910,				# The process ID.
# 	"ppid": 1308,				# The PID of the parent of this process.
# 	"rss": 36642816,			# Resident Set Size: number of bytes the process has in real memory. This is just the bytes which count toward text, data, or stack space. This does not include bytes which have not been demand-loaded in, or which are swapped out.
# 	"stime": 0.01,				# Amount of time that this process has been scheduled in kernel mode, measured in absolute number of seconds
# 	"tty_nr": 34845,			# The controlling terminal of the process. (The minor device number is contained in the combination of bits 31 to 20 and 7 to 0; the major device number is in bits 15 to 8.)
# 	"utime": 0.18,				# Amount of time that this process has been scheduled in user mode, measured in absolute number of seconds
# 	"vsize": 109965312			# Virtual memory range in bytes
# }
#
def get_proc_pid_stat(pid:int, c = None) -> dict:
	assert isinstance(pid, int)
	assert pid > 0

	stdout, stderr, exitcode = jk_sysinfo.run(c, "cat /proc/" + str(pid) + "/stat")
	stdout = stdout.strip()

	# split into parts and extract fileName

	parts = stdout.split(" ")
	items = [ parts[0] ]
	assert parts[1][0] == "("
	fileName = None
	for i in range(1, len(parts)):
		if parts[i][-1] == ")":
			# end of file name found
			fileName = " ".join(parts[1:i+1])
			fileName = fileName[1:-1]
			items.extend(parts[i+1:])
			break
	assert fileName is not None
	assert len(items) == 51

	ret = {}
	for _i, _key, _keyResult, _parser, _iFactor in _VALUE_SPECS_STAT:
		_vpart = items[_i]
		if (_parser is not None) and (_parser is not str):
			ret[_keyResult] = (int(_vpart) * _iFactor) if (_parser == int) else _parser(_vpart)
		else:
			ret[_keyResult] = _vpart

	return ret
#




# see: "man proc"
#_VALUE_SPECS_IO = (
##	POS		MAN PAGE KEY NAME			KEY NAME TO USE				TYPE	FACTOR
#	#(	0,	"rchar",					"rchar",					int,	1			),	# The number of bytes which this task has caused to be read from storage. This is simply the sum of bytes which this process passed to read(2) and similar system calls. It includes things such as terminal I/O and is unaffected by whether or not actual physical disk I/O was required (the read might have been satisfied from pagecache).
#	#(	1,	"wchar",					"wchar",					int,	1			),	# The number of bytes which this task has caused, or shall cause to be written to disk. Similar caveats apply here as with rchar.
#	#(	2,	"syscr",					"syscr",					int,	1			),	# Attempt to count the number of read I/O operations — that is, system calls such as read(2) and pread(2).
#	#(	3,	"syscw",					"syscw",					int,	1			),	# Attempt to count the number of write I/O operations — that is, system calls such as write(2) and pwrite(2).
#	(	4,	"read_bytes",				"read_bytes",				int,	1			),	# Attempt to count the number of bytes which this process really did cause to be fetched from the storage layer. This is accurate for block-backed filesystems.
#	(	5,	"write_bytes",				"write_bytes",				int,	1			),	# Attempt to count the number of bytes which this process caused to be sent to the storage layer.
#	#(	6,	"cancelled_write_bytes",	"cancelled_write_bytes",	int,	1			),	# The big inaccuracy here is truncate. If a process writes 1MB to a file and then deletes the file, it will in fact perform no writeout. But it will have been accounted as having caused 1MB of write. In other words: this field represents the number of bytes which this process caused to not happen, by truncating pagecache. A task can cause "negative" I/O too. If this task truncates some dirty pagecache, some I/O which another task has been accounted for (in its write_bytes) will not be happening.
#)
_VALUE_PARSERS_IO = {
	"read_bytes": jk_cmdoutputparsinghelper.ValueParserDef("read_bytes", "io_read_bytes", int),		# Attempt to count the number of bytes which this process really did cause to be fetched from the storage layer. This is accurate for block-backed filesystems.
	"write_bytes": jk_cmdoutputparsinghelper.ValueParserDef("write_bytes", "io_write_bytes", int),	# Attempt to count the number of bytes which this process caused to be sent to the storage layer.
}


#
# Returns something like this:
#
# {
#	"read_bytes": 123,
#	"write_bytes": 45678
# }
#
def get_proc_pid_io(pid:int, c = None) -> dict:
	assert isinstance(pid, int)
	assert pid > 0

	stdout, stderr, exitcode = jk_sysinfo.run(c, "cat /proc/" + str(pid) + "/io")
	stdout = stdout.strip()

	stdoutLines = stdout.split("\n")

	ret = _LINE_PARSER.parseLinesReturnDict(stdoutLines, valueParserMap=_VALUE_PARSERS_IO)
	return ret
#









