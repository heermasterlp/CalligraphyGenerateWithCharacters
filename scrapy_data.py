# coding: utf-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import json


class OnLineDictScrapy(object):
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options, executable_path="../geckodriver")

    def __del__(self):
        self.driver.quit()

    def get_page_source(self, url):
        if url == "":
            print("Search url should not be none!")
            return

        self.driver.get(url)
        if self.driver.page_source:
            return self.driver.page_source
        else:
            return

    def parse_html(self, page_source):
        if page_source is None:
            print("Page source is none!")
            return
        # result dict
        result_dict = {}
        html = BeautifulSoup(page_source, 'html.parser')

        # char
        char_str = ""
        divs = html.find_all("div", class_="word-bg")
        if divs:
            char_str = divs[0].get_text()
            print("char: ", char_str)


        # Radical, STROKE_COUNT, STRUCTURE, TYPE, PINYINS, KEY_RADICAL
        stroke_count = ""
        stroke_order = ""
        structure = ""
        type = "character"
        pinyins = ""
        key_radical = ""

        divs = html.find_all("div", class_="word-attribute")
        if divs:
            print("div len: ", len(divs))

            for div in divs:
                # pinyin
                if "拼音" in div.get_text():
                    pinyins = div.get_text().replace("\n", " ").replace("拼音", "")

                # 部首
                if "部首" in div.get_text() and "简体部首" not in div.get_text() and "繁体部首" not in div.get_text():
                    key_radical = div.get_text().replace("\n", "").replace("部首", "").replace("部", "")
                # 笔画
                if "笔画" in div.get_text():
                    bihua_a = div.find_all("a")
                    if bihua_a:
                        stroke_count = bihua_a[0].get_text()
                # 结构
                if "结构" in div.get_text():
                    structure = div.get_text().replace("\n", "").replace("结构", "")
                # 笔顺
                if "笔顺" in div.get_text():
                    stroke_order = div.get_text().replace("\n", "").replace("笔顺", "")


                result_dict["TAG"] = char_str
                result_dict["PINYIN"] = pinyins
                result_dict["KEY_RADICAL"] = key_radical
                result_dict["STROKE_COUNT"] = stroke_count
                result_dict["STROKE_ORDER"] = stroke_order
                result_dict["STRUCTURE"] = structure

        return result_dict





def run():
    # base url
    base_url = "https://www.koolearn.com/zidian/zi_%d.html"

    max_page = 25903

    app = OnLineDictScrapy()

    result = []

    for id in range(1, max_page+1):
        url = (base_url % id)
        print(url)

        page_source = app.get_page_source(url)

        dict = app.parse_html(page_source)
        result.append(dict)
        print(dict)

        time.sleep(1.5)

    with open("scrapy_result.json", "w", encoding="utf8") as outfile:
        json.dump(result, outfile, ensure_ascii=False)




if __name__ == '__main__':
    run()

    # url = "https://www.koolearn.com/zidian/zi_1.html"
    #
    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options, executable_path="../geckodriver")
    #
    # driver.get(url)
    #
    # html = BeautifulSoup(driver.page_source, features="html.parser")
    #
    # divs = html.find_all("div", class_="word-bg")
    # if divs:
    #     print(len(divs))
    #     print(divs[0].get_text())
    # else:
    #     print("not find divs")
    #
    # # print(driver.page_source)
    #
    # driver.quit()

