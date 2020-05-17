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
import os

from gauto_profiler import profiler
from gauto_profiler import  config

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config.setup(serial="5366a3d3", output_path="output", html_save_path="output/render.html")
profiler.run(300)
```