import sys
import os
import subprocess
import shlex
import psutil
import time
import shutil

pid=psutil.pid_exists(int(sys.argv[1]))
# temppath=str(sys.argv[2])
temppath=os.path.abspath(os.path.dirname("train_test.py"))+'/data/tempdataset'
time.sleep(10)
if pid:
    # print(pid)
    a = shlex.split('python pie/dataset/monitor.py ' + sys.argv[1])
    subprocess.Popen(a)
else:
    # print(pid)
    shutil.rmtree(temppath)
