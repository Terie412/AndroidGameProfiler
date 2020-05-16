## AndroidGameProfiler
![symbol](https://img.shields.io/badge/qintianchen-gauto--profiler-orange)
[![0.1.1](https://img.shields.io/badge/version-v0.1.1-blue)](https://pypi.org/manage/project/gauto-profiler/releases/) 

[中文文档](./README_cn.md)

A python library that captures the three basic capabilities of a game on Android -- Total PSS (physical memory used by applications, including proportionally Shared library memory), CPU usage, and FPS (frame rate).

The above data are all obtained by adb tool.

## Install

```shell script
pip install gauto-profiler
```

## Usage

```python
from gauto_profiler.mem import *
from gauto_profiler.cpu import *
from gauto_profiler.fps import *
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ["ANDROID_SERIAL"] = "5366a3d3" # the serial of the android device you are willing to test

# Specify the output directory.
# All these threads will share a directory, so once one thread has specify the path, there is no need to do so for the subsequent threads
mem_thread = MemRecorder("output")
cpu_thread = CPURecorder()
fps_thread = FPSRecorder()

# start running
mem_thread.start()
cpu_thread.start()
fps_thread.start()

time.sleep(300) # run for 5 mins

# stop
mem_thread.stop()
cpu_thread.stop()
fps_thread.stop()
mem_thread.join()
cpu_thread.join()
fps_thread.join()

print("All threads have stopped")
```