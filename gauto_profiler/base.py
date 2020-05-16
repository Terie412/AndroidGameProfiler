from gauto_profiler.utils.adb_tool import *
import logging
import os
import threading
import time
import re

logger = logging.getLogger("gauto")

class RecorderBase(threading.Thread):
    __is_init = False

    serial = None
    pid = None
    win_size = None
    sdk_version = None
    pkg_name = None
    main_activity = None
    abi = None
    output_path = None

    def __init__(self, path):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()
        if RecorderBase.output_path is None and path is not None:
            RecorderBase.output_path = path
        elif RecorderBase.output_path is not None and path is not None and path != RecorderBase.output_path:
            logger.warning(f"\n{self.__class__.__name__}:It is supposed to put all record in a single directory")
        if not RecorderBase.__is_init:
            self.init()

    def run(self):
        while self.__running.isSet():
            self.step()
            self.record()

    def step(self):
        logger.warning(f"{self.__class__.__name__}:Please override step(self) or the thread will be end quickly")
        self.stop()

    def record(self):
        print(f"you should override this method to record your data")
        time.sleep(2)
        pass

    def stop(self):
        self.__running.clear()

    # region 初始化一些全局常量
    def init(self):
        RecorderBase.serial = os.environ.get("ANDROID_SERIAL", None)
        logger.info(f"{'serial':<15} = {RecorderBase.serial}")
        self.init_win_size()
        self.init_sdk_version()
        self.init_abi()
        self.init_pkg_name()
        self.init_activity()
        self.init_pid()

    @staticmethod
    def init_win_size():
        ret = excute_adb_process("shell wm size", RecorderBase.serial)
        ret = ret.split("\n")[0]
        matches = re.search(r"\d+x\d+", ret)
        if matches:
            ratio = matches.group(0).split("x")
            num1, num2 = int(ratio[0]), int(ratio[1])
            RecorderBase.win_size = (num1, num2) if num1 > num2 else (num2, num1)
            logger.info(f"{'win_size':<15} = {RecorderBase.win_size}")
        else:
            raise Exception("Failed to init win_size")

    @staticmethod
    def init_sdk_version():
        sdk_version = excute_adb_process("shell getprop ro.build.version.sdk").rstrip("\r\n\n")
        if str.isalnum(sdk_version):
            RecorderBase.sdk_version = int(sdk_version)
            logger.info(f"{'sdk_version':<15} = {RecorderBase.sdk_version}")
        else:
            raise Exception("Failed to init sdk_version")

    @staticmethod
    def init_pkg_name():
        ret = excute_adb_process("shell dumpsys activity activities | findstr mResumedActivity", RecorderBase.serial)
        line = ret.split("\n")[0]
        pattern = re.compile(r"(\w+\.*)+/(\w*\.*)+")
        match = pattern.search(line)
        if match:
            ret = match.group(0).split("/")[0]
            RecorderBase.pkg_name = ret
            logger.info(f"{'package name':<15} = {RecorderBase.pkg_name}")
        else:
            raise Exception("Failed to init package name")

    @staticmethod
    def init_activity():
        cmd = f'shell dumpsys SurfaceFlinger | findstr {RecorderBase.pkg_name}'
        ret = excute_adb_process(cmd, RecorderBase.serial)
        lines = ret.split('\n')
        line = ""
        for l in lines:
            if len(l) > 2 and "layer" in l.lower():
                line = l
        pattern = re.compile(r'(\w+\.*)+/([^\s\])]\.*)+')
        match = pattern.search(line)
        if match:
            RecorderBase.main_activity = match.group(0)
            logger.info(f"{'Main Activity':<15} = {RecorderBase.main_activity}")
        else:
            raise Exception("Failed to init Main Activity")

    @staticmethod
    def init_pid():
        cmd = f"shell ps | findstr {RecorderBase.pkg_name}"
        ret = excute_adb_process(cmd, RecorderBase.serial)
        if len(ret) < 20:
            cmd = f"shell ps -ef | findstr {RecorderBase.pkg_name}"
            ret = excute_adb_process(cmd, RecorderBase.serial)
        ret = ret.split()[1]
        RecorderBase.pid = ret
        logger.info(f"{'pid':<15} = {RecorderBase.pid}")

    @staticmethod
    def init_abi():
        abi = excute_adb_process("shell getprop ro.product.cpu.abi", RecorderBase.serial)
        abi = abi.split("\n")[0].rstrip("\r")
        RecorderBase.abi = abi
        logger.info(f"{'abi':<15} = {RecorderBase.abi}")

    # endregion
