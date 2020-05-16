import logging

def init_logger():
    fmt = '%(asctime)s - %(levelname)7s - %(filename)20s:%(lineno)-3s $$ %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)  # 为handler添加formatter
    logger = logging.getLogger("gauto")  # 获取名为wetest的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(logging.DEBUG)

init_logger()
