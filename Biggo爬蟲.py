from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import sqlite3

options = Options()
options.add_argument("--disable-notifications")


driver = webdriver.Chrome('./chromedriver', chrome_options=options)

ECs = {  # 所有通路
    'pchome':  "tw_ec_pchome24h",
    'momo': "tw_pec_momoshop"
}
biggo_base_url = "https://biggo.com.tw/s/"


def get_url_by_goods_name(goods_name, ec):
    """組成類似像是 https://biggo.com.tw/s/biore%20%E6%B4%97%E9%9D%A2%E4%B9%B3/?&m=cp&c[]=tw_pec_momoshop 的格式"""
    EC = ECs.get(ec)
    url = f'{biggo_base_url}{goods_name}/?&m=cp&c[]={EC}'
    return url


def wait_until(xpath: str):
    element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(("xpath", xpath))
    )
    return element


def get_goods_name(brand, item_name):
    goods_name = f'{brand} {item_name}'
    return goods_name


def get_goods_info(url):
    EC = ""
    name = ""
    price = ""
    driver.get(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    response = requests.get(driver.current_url, headers=headers)
    cosmetic_list = []
    soup = BeautifulSoup(response.text, 'lxml')

    btn_dropdowns = soup.find_all('div', 'multple_spec_btn _dropdown ml10')
    if btn_dropdowns != []:
        muti_dropdown_btn = wait_until("/html/body/div[3]/div/div/div[2]/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div")
        muti_dropdown_btn.click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')

    info_items = soup.find_all('div', 'col-12 product-row')
    for item in info_items:
        muti_btn = item.find('div', 'multple_spec_dropdown d-block _dropdown-menu')
        if muti_btn != None:
            main_name = item.find('div', 'list-product-name line-clamp-2').a.text.strip()
            price = muti_btn.find('div', 'onerow').text.split(' ')[1]
            sub_name = muti_btn.find('div', 'onerow').text.split(' ')[0]
            EC = item.find('div', 'store-name-wrap', 'store').text.strip()
            name = main_name,sub_name
            cosmetic_info = dict(品名=name, 價格=price, 通路=EC)
            cosmetic_list.append(cosmetic_info)
        else:
            name = item.find('div', 'list-product-name line-clamp-2').a.text.strip()
            price = item.find('div', 'd-flex flex-wrap align-items-center', 'price').a.text.strip()
            EC = item.find('div', 'store-name-wrap', 'store').text.strip()
            cosmetic_info = dict(品名=name, 價格=price, 通路=EC)
            cosmetic_list.append(cosmetic_info)

    for i in cosmetic_list:
        print(i)
    # print(cosmetic_list)
    return EC, name, price

# input? user 要如何提供 ec brand item_name 這些資訊
# output? 請 user 提供 excel sample

# 當多個 ec 時要如何處理

items = [
    {'ec': "momo", 'brand': "CLIO珂莉奧", 'item_name': "凝時美肌防沾染柔霧粉底液 精巧版"},
    {'ec': "pchome", 'brand': "CLIO珂莉奧", 'item_name': "凝時美肌防沾染柔霧粉底液 精巧版"}
]

try:
    for item in items:
        goods_name = get_goods_name(item['brand'], item['item_name'])
        #print(goods_name)
        url = get_url_by_goods_name(goods_name, item['ec'])
        EC, name, price = get_goods_info(url)

        print(EC, name, price)
finally:
    driver.close()
