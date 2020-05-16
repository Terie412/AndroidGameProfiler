## AndroidGameProfiler
![symbol](https://img.shields.io/badge/qintianchen-gauto--profiler-orange)
[![0.1.1](https://img.shields.io/badge/version-v0.1.1-blue)](https://pypi.org/manage/project/gauto-profiler/releases/) 

一个python库，用来获取Android上游戏的三项基础性能——Total pss（应用占用的物理内存，包含比例分配的共享库占用的内存），cpu占用率和FPS（帧率）。

以上数据全部依赖adb获取。

## 安装

```shell script
pip install gauto-profiler
```

## 使用

```python
from gauto_profiler.mem import *
from gauto_profiler.cpu import *
from gauto_profiler.fps import *
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ["ANDROID_SERIAL"] = "5366a3d3" # 设置当前测试的安卓设备序列号

# 指定输出目录。三个线程会公用一个目录，所以其中一个线程指定过之后，后面就不用再指定了
mem_thread = MemRecorder("output")
cpu_thread = CPURecorder()
fps_thread = FPSRecorder()

# 开始运行
mem_thread.start()
cpu_thread.start()
fps_thread.start()

time.sleep(300) # 运行 5 分钟

# 停止
mem_thread.stop()
cpu_thread.stop()
fps_thread.stop()
mem_thread.join()
cpu_thread.join()
fps_thread.join()

print("All threads have stopped")
```