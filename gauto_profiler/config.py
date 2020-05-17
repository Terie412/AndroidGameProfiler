import os

global_config = {}

def setup(serial = None, output_path = None, html_save_path = None):
    if serial is not None:
        global_config["serial"] = serial
    if output_path is not None:
        global_config["output_path"] = output_path
    if html_save_path is not None:
        global_config["html_save_path"] = html_save_path
