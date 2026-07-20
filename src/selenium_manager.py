import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DriverManager:
        
    def __init__(self):
        self.local = threading.local()

        self.drivers = []

        self.lock = threading.Lock()


    def create_driver(self):
        
        options = Options()
        options.add_argument("--headless")                  #  无头模式，就是不打开浏览器
        options.add_argument("--no-sandbox")                #  浏览器安全隔离机制,限制浏览器进程权限
        options.add_argument("--disable-gpu")               #  不用GPU渲染，也无用
        options.add_argument("--disable-dev-shm-usage")     #  Linux /dev/shm共享内存不足时：让Chrome不要使用共享内存。
        
        driver = webdriver.Chrome(options=options)

        with self.lock:
            self.drivers.append(driver)

        return driver


    def get_driver(self):

        if not hasattr(
            self.local,
            "driver"
        ):

            self.local.driver = self.create_driver()


        return self.local.driver


    def close_all(self):

        with self.lock:

            drivers = self.drivers.copy()

            self.drivers.clear()


        for driver in drivers:

            try:
                driver.quit()

            except:
                pass


    def remove_driver(self):

        if not hasattr(
            self.local,
            "driver"
        ):
            return
        
        driver = self.local.driver

        try:
            driver.quit()

        except:
            pass


        with self.lock:

            if driver in self.drivers:

                self.drivers.remove(driver)


        del self.local.driver


driver_manager = DriverManager()