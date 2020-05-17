import logging
import math
import os

from pyecharts.charts import Line, Page, Gauge, Grid
from pyecharts import options as opts
import csv

logger = logging.getLogger("gauto")


def read_csv(file_name):
    if not os.path.exists(file_name):
        logger.error(f"file:'{file_name}' not exist")
        return [0], [0]
    with open(file_name, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        reader = list(reader)

        x_data = []
        y_data = []
        time_start = reader[1][0]
        for i in range(1, len(reader)):
            line = reader[i]
            x_data.append(float(line[0]) - float(time_start))
            y_data.append(float(line[1]))
        return x_data, y_data


def get_line(data_x, data_y, line_name=""):
    line = Line()
    line.set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    line.add_xaxis(xaxis_data=data_x)
    line.add_yaxis(
        series_name=line_name,
        y_axis=data_y,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
        is_smooth=True
    )
    return line


def get_gauge(data_y: list, gauge_name=""):
    gauge = Gauge()
    gauge.add(
        gauge_name,
        [(gauge_name, (sum(data_y) * 100) / (len(data_y) * max(data_y)))],
        axisline_opts=opts.AxisLineOpts(
            linestyle_opts=opts.LineStyleOpts(
                color=[(0.3, "#67e0e3"), (0.7, "#37a2da"), (1, "#fd666d")], width=30
            ),
        ),
    )
    gauge.set_global_opts(
        # title_opts=opts.TitleOpts(title=gauge_name),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    return gauge


def render_html(output_path, html_name="render.html"):
    cpu_x, cpu_y = read_csv(output_path + "/cpu_info.csv")
    fps_x, fps_y = read_csv(output_path + "/fps_info.csv")
    mem_x, mem_y = read_csv(output_path + "/mem_info.csv")

    cpu_line = get_line(cpu_x, cpu_y, "CPU占用率(%)")
    fps_line = get_line(fps_x, fps_y, "FPS")
    mem_line = get_line(mem_x, mem_y, "Total PSS")

    cpu_gauge = get_gauge(cpu_y, "CPU占用率平均值")
    fps_gauge = get_gauge(fps_y, "FPS平均值")
    mem_gauge = get_gauge(mem_y, "Total PSS平均值")

    page = Page()
    page.add(cpu_gauge)
    page.add(fps_gauge)
    page.add(mem_gauge)
    page.add(cpu_line).add(fps_line).add(mem_line)
    page.render(path=html_name)


