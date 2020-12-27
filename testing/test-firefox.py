#!/usr/bin/python3


import typing
import os
import sys
import time

import jk_json
import jk_sysinfo
import jk_utils

from jk_appmonitoring import *




UID = os.getuid()



rpList = RProcessList()
rpList.update()

rpList2 = rpList.filter(RProcessFilter(uid=UID, cmd="/usr/lib/firefox/firefox"))
rpList2.enrichWithMoreData()
#rpList2.dump()

print()
summary = rpList2.calcSummary()
for k in sorted(summary.keys()):
	v = summary[k]
	if isinstance(v, jk_utils.AmountOfBytes):
		print(k, ":", v.toStr(magnitude="M"))
	else:
		print(k, ":", v)
print()







