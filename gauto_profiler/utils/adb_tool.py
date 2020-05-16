import os
import logging
import subprocess
import time

logger = logging.getLogger("gauto")


def excute_adb(cmd, serial=None):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)
    file = os.popen(command)
    return file


def excute_adb_process_daemon(cmd, shell=False, serial=None, sleep=3, needStdout=True):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)
    if needStdout is True:
        p = subprocess.Popen(command, shell=shell, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(command, shell=shell)
    time.sleep(sleep)
    return p


def excute_adb_process(cmd, serial=None):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)

    p = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    lines = p.stdout.readlines()
    ret = ""
    for line in lines:
        ret += line.decode() + "\n"
    else:
        return ret



