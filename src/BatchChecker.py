#!/usr/bin/python

import os
import sys

if len(sys.argv[0].split('/')) > 2 :
    os.chdir(sys.argv[0].rsplit('/', 2)[0])

from Modules import Config
from Modules.Db import Batch
from Modules import Scheduler

C = Config.Config()
D = Batch(C.Db)
S = Scheduler.Scheduler(C.Scheduler, D)

if not S.isDaemonRunning() :
    print "Starting"
    S.process()
    print "End"