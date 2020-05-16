from gauto_profiler.base import *


class CPURecorder(RecorderBase):
    def __init__(self, path=None):
        super().__init__(path)
        self.time_stamp = 0
        self.data = None
        self.if_head_written = False

    def step(self):
        self.get_cpu_info()
        time.sleep(1)

    def record(self):
        if not os.path.exists(RecorderBase.output_path):
            os.mkdir(RecorderBase.output_path)

        file_name = RecorderBase.output_path + "/cpu_info.csv"
        with open(file_name, "a+") as fp:
            if not self.if_head_written:
                fp.write("time stamp,cpu usage(%)\n")
            fp.write(f"{self.time_stamp},{self.data}\n")

    def get_cpu_info(self):
        self.time_stamp = time.time_ns() / 1E6 # ms
        if RecorderBase.sdk_version <= 23:
            cpu_cmd = f"shell top -n 1 -m 3 -d 0.1 | findstr {RecorderBase.pid}"
            cpu_info_string = excute_adb_process(cpu_cmd, RecorderBase.serial)
            cpu_info_list = cpu_info_string.split()
            self.data = cpu_info_list[2].rstrip().lstrip().lstrip("%")
            logger.info(f"cpu usage = {self.data}")
        else:
            cpu_cmd = f"shell top -n 1 -m 3 | findstr {RecorderBase.pid}"
            cpu_info_string = excute_adb_process(cpu_cmd, RecorderBase.serial)
            cpu_info_list = cpu_info_string.split()
            self.data = cpu_info_list[8].rstrip().lstrip()
            if self.data.replace(".", "").isalnum():
                self.data = int(float(self.data))
                logger.info(f"cpu usage = {self.data}")
            else:
                logger.warning(f"Failed to get cpu info")
                return
