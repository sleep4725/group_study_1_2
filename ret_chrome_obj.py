from selenium import webdriver


class ChromeDriverObj:

    DRIVER_PATH = "./get_chrome_driver/chromedriver"

    # headless 타입의 selenium object 를 반환한다.
    @classmethod
    def get_chrome_obj(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("disable-gpu")

        chrome_driver = webdriver.Chrome(ChromeDriverObj.DRIVER_PATH, chrome_options = chrome_options)
        return chrome_driver
