import time
from gauto_profiler import config
from gauto_profiler.core.chart import *
from gauto_profiler.core.cpu import CPURecorder
from gauto_profiler.core.fps import FPSRecorder
from gauto_profiler.core.mem import MemRecorder

def run(duration):
    os.environ["ANDROID_SERIAL"] = config.global_config["serial"]

    mem_thread = MemRecorder(config.global_config["output_path"])
    mem_thread.start()
    cpu_thread = CPURecorder()
    cpu_thread.start()
    fps_thread = FPSRecorder()
    fps_thread.start()

    time.sleep(duration)

    mem_thread.stop()
    fps_thread.stop()
    cpu_thread.stop()
    mem_thread.join()
    fps_thread.join()
    cpu_thread.join()

    render_html(config.global_config["output_path"], config.global_config["html_save_path"])
