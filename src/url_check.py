import requests, urllib3
from config import TIMEOUT
from .selenium_manager import driver_manager
from utils.threads_pool import run_threads_pool
from selenium.webdriver.support.ui import WebDriverWait

urllib3.disable_warnings()

def request_check(url):
    
    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    }

    try:

        r = requests.get(
            url,
            timeout=TIMEOUT,
            verify=False,
            allow_redirects=True
            ,headers = HEADERS
        )

        status_code = r.status_code

        if status_code < 400:
            level = "alive"

        elif r.status_code in [401,403,405]:
            level = "possible"

        elif r.status_code == 404:
            level = "dead"
        
        else:
            level = "possible"

        result = {
            "url": url,
            "status": r.status_code,
            "alive":level,
            "message": "success"
        }

        print(
            f"url:{url}\n"
            f"status:{r.status_code}\n"
            f"alive:{result['alive']}\n"
            "----------------"
        )

        return result

    except Exception as e:

        result = {
            "url": url,
            "status": None,
            "alive": "dead",
            "message": str(e)
        }

        print(
            f"url:{url}\n"
            f"status:None\n"
            f"alive:False"
            "----------------\n"
        )

        return result


def is_real_page(title, source):
        
    if not source:
        return False

    if len(source.strip()) < 100:
        return False

    bk_lists = [
        "404 not found",
        "welcome to nginx",
        "test page"
    ]

    text = (
        title + source[:500]
    ).lower()

    for word in bk_lists:

        if word in text:
            return False
        
    return True


def selenium_check(url):
    
    try:

        driver = driver_manager.get_driver()

        driver.get(url)

        WebDriverWait(
            driver,
            5
        ).until(
            lambda d:
            d.execute_script(
                "return document.readyState"
            ) == "complete"
        )
        
        title = driver.title.strip()
        html = driver.page_source

        if is_real_page(title, html):
            level = "alive"
        
        else:
            level = "dead"

        return {
            "url":url,
            "title":title,
            "alive":level
        }
    
    except Exception as e:

        driver_manager.remove_driver()

        return {
            "url":url,
            "title":None,
            "alive":"possible",
            "message":str(e)
        }


def check(urls, tr, ts):

    request_res = run_threads_pool(request_check, urls, tr)

    check_urls = []

    for item in request_res:
        if item["alive"] != "dead":
            check_urls.append(item["url"])

    selenium_res = run_threads_pool(selenium_check, check_urls, ts)

    return request_res, selenium_res
