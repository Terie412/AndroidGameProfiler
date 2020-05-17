from gauto_profiler.core.base import *


class MemRecorder(RecorderBase):
    def __init__(self, path=None):
        super().__init__(path)
        self.time_stamp = 0
        self.data = None
        self.if_head_written = False

    def step(self):
        self.get_memory_info()
        time.sleep(1)

    def record(self):
        if not os.path.exists(RecorderBase.output_path):
            os.mkdir(RecorderBase.output_path)

        file_name = RecorderBase.output_path + "/mem_info.csv"
        with open(file_name, "a+") as fp:
            if not self.if_head_written:
                fp.write("time stamp,mem(kB),mem(MB)\n")
                self.if_head_written = True
            fp.write(f"{self.time_stamp},{self.data},{self.data/1024}\n")

    def get_memory_info(self):
        self.time_stamp = time.time_ns()/1E9 # s
        cmd = f"shell dumpsys meminfo {RecorderBase.pkg_name} | findstr TOTAL"
        mem_info_string = excute_adb_process(cmd, RecorderBase.serial)
        mem_info_list = mem_info_string.split('\n')
        for i in range(len(mem_info_list)):
            info = mem_info_list[i]
            if 'TOTAL' in info:
                self.data = int(re.findall(r"\d+", info)[0])
                logger.info(f"Total PSS : {self.data} kB = {self.data/1024} MB")
                break
            else:
                logger.error(f"Failed to get meminfo")
