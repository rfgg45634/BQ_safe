import os

REQUEST_THREADS = 5
# request 请求默认线程数

SELENIUM_THREADS = 1
# selenium 请求默认线程数

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs"
)

# 默认输出文件目录

TIMEOUT = 5