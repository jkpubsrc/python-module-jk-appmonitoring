#!/usr/bin/python3


import time
import threading

import jk_json

from jk_appmonitoring import *


def threadRun():
	time.sleep(1000)
#


#t = threading.Thread(target=threadRun)
#t.start()




x = AppCPUInfo()

jOwnProcessInfo, jChildProcessInfos = x.getData()

jk_json.prettyPrint(jOwnProcessInfo)




input()





