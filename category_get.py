from ret_chrome_obj import ChromeDriverObj
from bs4 import BeautifulSoup
import pprint as ppr


class CategoryGet:

    @classmethod
    def get_config_category(cls):
        req_url = "https://finance.naver.com/sise/sise_market_sum.nhn"
        chrome_driver = ChromeDriverObj.get_chrome_obj()
        chrome_driver.get(url=req_url)
        chrome_driver.implicitly_wait(3)

        bs_object = BeautifulSoup(chrome_driver.page_source, "html.parser")
        items_list = bs_object.select_one("table.item_list > tbody").select("tr > td")
        category_dict = dict()

        c = 0
        for i in items_list:
            input_data = i.select_one("input")

            if input_data:
                input_data = input_data.attrs["value"]
                label_data = i.select_one("label").text
                category_dict[c+1] = {
                    "eng": input_data,
                    "kor": label_data
                }
                c += 1

        if chrome_driver:
            chrome_driver.close()

        if category_dict:
            ppr.pprint(category_dict)
            return category_dict
        else:
            exit(1)
