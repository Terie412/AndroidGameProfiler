from gauto_profiler.core.base import *


class FPSRecorder(RecorderBase):
    def __init__(self, path=None):
        super().__init__(path)
        self.time_stamp = 0
        self.data = None
        self.if_head_written = False

    def step(self):
        self.get_fps_info()
        time.sleep(1)

    def record(self):
        if not os.path.exists(RecorderBase.output_path):
            os.mkdir(RecorderBase.output_path)

        file_name = RecorderBase.output_path + "/fps_info.csv"
        with open(file_name, "a+") as fp:
            if not self.if_head_written:
                fp.write("time stamp,fps(frames per sec)\n")
                self.if_head_written = True
            fp.write(f"{self.time_stamp},{self.data}\n")

    def get_fps_info(self):
        self.time_stamp = time.time_ns() / 1E9 # s
        clear = f'shell dumpsys SurfaceFlinger --latency -clear'
        excute_adb_process(clear, RecorderBase.serial)
        pro = f" - {RecorderBase.main_activity}" if self.sdk_version > 23 else ""
        cmd = f"shell dumpsys SurfaceFlinger --latency 'SurfaceView{pro}'"
        ret = excute_adb_process(cmd, RecorderBase.serial)

        res = ret.replace("\n\n", "\n").split("\n", -1)
        if len(re.findall(r"\d+", res[0])) == 0:
            return 0

        res = res[96:127]
        try:
            del (res[0])
            del (res[-1])
        except:
            pass

        # print(len(res))
        a = re.findall(r"\d+", res[-1])[0]
        b = re.findall(r"\d+", res[0])[0]
        totalFpsTime = (int(a) - int(b)) / 1E9

        fps = (len(res) - 1) / totalFpsTime
        self.data = fps
        logger.info(f"fps = {self.data}")
