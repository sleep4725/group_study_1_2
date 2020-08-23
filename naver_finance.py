"""
fieldIds=quant&fieldIds=per&fieldIds=ask_sell&fieldIds=roe&fieldIds=frgn_rate&fieldIds=listed_stock_cnt
"""
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import altair_viewer as alt_view
import pandas as pd

from ret_chrome_obj import ChromeDriverObj
from category_get import CategoryGet


class NaverFinance:


    def __init__(self):
        self.category = CategoryGet.get_config_category()
        self.url = NaverFinance.get_url()
        self.chrome_driver = ChromeDriverObj.get_chrome_obj()
        self.result_total_data = list()

    def get_stock_rank(self):
        print ("======================================")
        print ("적용선택__(0 : 끝내기 입니다.)")
        print ("최소 1개, 최대 6개까지만 선택가능합니다.")
        arg_count = 0
        arg_list = list()

        while True:
            if arg_count == 6:
                break

            choice = int(input(": "))
            if 1 <= choice <= 27:
                argu = "fieldIds={}".format(self.category[choice]["eng"])
                arg_list.append(argu)
                arg_count += 1
            else:
                if choice == 0:
                    break
                else:
                    print ("1 ~ 27 까지의 값만 입력하실 수 있습니다.")

        argu_str = "&".join(arg_list)
        req_url = self.url + NaverFinance.get_param() + argu_str
        print (req_url)
        self.stock_rank_get(req_url=req_url)

    def stock_rank_get(self, req_url):
        self.chrome_driver.get(url=req_url)
        self.chrome_driver.implicitly_wait(3)
        bs_object = BeautifulSoup(self.chrome_driver.page_source, "html.parser")

        self.chrome_driver.close()

        thead = [ x.string for x in bs_object.select_one("table.type_2 > thead > tr").select("th")]
        thead = thead[0: len(thead)-1]

        print (thead)
        tbody  = bs_object.select_one("table.type_2 > tbody").select("tr")
        tmp_tbody = tbody[1:]

        jump_index = 0
        while jump_index < len(tmp_tbody):
            for i in tmp_tbody[jump_index: jump_index + 5]:
                td = i.select("td")
                td = td[0:len(td)-1]   # 토론실 값은 제외
                tmp_dict = dict()
                for d, t in zip(td, thead):
                    result = str(d.text).strip("\n").strip("\t").rstrip("\n")
                    if t == "현재가":
                        result = result.replace(",", "")
                        result = int(result)

                    tmp_dict[t] = result

                self.result_total_data.append(tmp_dict)
            jump_index += 8

    def bar_chart(self):
        tmp = {
            "a": list(),
            "b": list()
        }
        for x in self.result_total_data[0:10]:
            tmp["a"].append(x["종목명"])
            tmp["b"].append(x["현재가"])

        tmp = pd.DataFrame(tmp)

        bar_chart = alt.Chart(tmp).mark_bar().encode(
            x="a",
            y="b"
        )

        bar_chart.save("./get_graph_data/stock.html")

    @classmethod
    def get_url(cls):
        JSON_FILE = "./get_config/info.json"
        result = os.path.isfile(JSON_FILE)
        if result:
            with open(JSON_FILE, "r", encoding="utf-8") as json_file:
                url_info = json.load(json_file)
                json_file.close()

            return url_info["req_url"]
        else:
            exit(1)

    @classmethod
    def get_param(cls):
        url_param = urlencode({
            "menu": "market_sum",
            "returnUrl": "http://finance.naver.com/sise/sise_market_sum.nhn",
        })

        ## page 처리 argu 추가
        return url_param +"%3F%26page%3D1&"

if __name__ == "__main__":
    naver_finance_object = NaverFinance()
    naver_finance_object.get_stock_rank()
    naver_finance_object.bar_chart()