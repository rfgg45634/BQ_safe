import argparse, os
from src.scanner import scanner
from utils.file_clean import file_clean
from src.selenium_manager import driver_manager
from config import REQUEST_THREADS, SELENIUM_THREADS, OUTPUT_DIR

def parser_args():
    parser = argparse.ArgumentParser(
        description = "一个小型的URL资产检测工具"
    )

    parser.add_argument(
        "-f",
        "--file",
        required = True, 
        help = "输入文件，目前是必须提供的"
    )

    parser.add_argument(
        "-o", 
        "--output", 
        help = "输出文件名，固定为output文件夹下"
    )

    parser.add_argument(
        "-tr",
        "--request_threads",
        type = int,
        help = "request请求线程数，默认为5"
    )

    parser.add_argument(
        "-ts",
        "--selenium_threads",
        type = int,
        help = "selenium请求线程数，默认为1"
    )

    return parser.parse_args()
    # 对参数的处理函数

def main():

    args = parser_args()

    if not os.path.exists(args.file):
        raise FileNotFoundError(
            "文件不存在"
        )
    tr = args.request_threads or REQUEST_THREADS
    ts = args.selenium_threads or SELENIUM_THREADS

    config = {
        "输入文件：":args.file,
        "输出文件：":OUTPUT_DIR,
        "request请求线程数：":tr,
        "selenium请求线程：":ts
    }

    for k,v in config.items():
        print(f"{k}{v}")
        
    confirm = input(
        "确认开始扫描?(y/n):"
    )

    if confirm == "y":
        urls = file_clean(args.file)
        total = len(urls)
        print(f"开始扫描,共{total}个数据")
        try:
            scanner(urls, tr, ts, args.output)
        finally:
            driver_manager.close_all()

    else:
        print("退出")
    
    return

if __name__== "__main__":
    main()