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
import os

from gauto_profiler import profiler
from gauto_profiler import  config

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config.setup(serial="5366a3d3", output_path="output", html_save_path="output/render.html")
profiler.run(300)
```