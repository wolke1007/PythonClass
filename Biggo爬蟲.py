from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree
from urllib.request import urlopen
import time
import requests
import pandas as pd

df = pd.read_excel("EC商品價格檢查表_CLIO.xlsx", names= ['中文名', ' ', 'CSM EC', 'WTS EC', 'MOMO', 'PCHome', 'Books', '蝦皮']) #讀取excel檔案,重新命名row name

options = Options()
options.add_argument("--disable-notifications")


driver = webdriver.Chrome('./chromedriver', chrome_options=options)

ECs = {  # 所有通路(momo除外)
    'CSM EC' : 'tw_ec_cosmed',
    'WTS EC' : 'tw_ec_watsons',
    'PCHome':  "tw_ec_pchome24h",
    'Books' : 'tw_pec_books'
}
biggo_base_url = "https://biggo.com.tw/s/"


def get_url_by_goods_name(goods_name, ec):
    """組成類似像是 https://biggo.com.tw/s/biore%20%E6%B4%97%E9%9D%A2%E4%B9%B3/?&m=cp&c[]=tw_pec_momoshop 的格式"""
    EC_name = ECs.get(ec)
    url = f'{biggo_base_url}{goods_name}/?&m=cp&c[]={EC_name}'
    return url

def get_momo_url_by_goods_name(goods_name):
    """組成類似像是 https://biggo.com.tw/s/biore%20%E6%B4%97%E9%9D%A2%E4%B9%B3/?&m=cp&c[]=tw_pec_momoshop 的格式"""
    url = f'{biggo_base_url}{goods_name}/?&m=cp&c[]=tw_pec_momoshop'
    return url


def wait_until(xpath: str):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    return element


def get_goods_name(item_name):
    goods_name = f'{item_name}'
    return goods_name



def get_goods_info(url):
    EC_name = ""
    name = ""
    price = ""
    driver.get(url)
    action = webdriver.ActionChains(driver)
    cosmetic_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    response = requests.get(driver.current_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    total_items = soup.find_all('div', 'product-row')
    htmlparser = etree.HTMLParser()
    #url = driver.current_url
    response = urlopen(driver.current_url) #原本是url
    tree = etree.parse(response, htmlparser)
    #xpathselector = "(//div[@class='d-flex w100'])[1]//div[@class='multple_spec_btn _dropdown ml10']"  # 第一個品項的下拉選單
    for index, each_item in enumerate(total_items, start=1):
        str_index = str(index)
        xpathselector = "(//div[@class='d-flex w100'])[" + str_index + "]//div[@class='multple_spec_btn _dropdown ml10']"
        btn_dropdowns = tree.xpath(xpathselector)
        if btn_dropdowns != []:
            muti_dropdown_btn = wait_until(xpathselector)
            action.move_to_element(muti_dropdown_btn)
            muti_dropdown_btn.click()
            time.sleep(0.5)
            muti_dropdown_btn.click()

    soup = BeautifulSoup(driver.page_source, 'lxml')

    info_items = soup.find_all('div', 'product-row')
    if info_items == []:
        EC_name='找不到!!!'
    else:
        for item in info_items:
            muti_btn = item.find('div', 'multple_spec_dropdown _dropdown-menu')
            if muti_btn is not None:
                for btn in muti_btn:
                    main_name = item.find('div', 'list-product-name line-clamp-2').a.text.strip()
                    price = btn.text.split(' ')[-1]
                    sub_name = btn.text.split(' ')[0]
                    EC_name = item.find('div', 'store-name-wrap', 'store').text.strip()
                    name = main_name, sub_name
                    cosmetic_info = dict(品名=name, 價格=price, 通路=EC_name)
                    cosmetic_list.append(cosmetic_info)
            else:
                name = item.find('div', 'list-product-name line-clamp-2').a.text.strip()
                price = item.find('div', 'd-flex flex-wrap align-items-center', 'price').a.text.strip()
                EC_name = item.find('div', 'store-name-wrap', 'store').text.strip()
                cosmetic_info = dict(品名=name, 價格=price, 通路=EC_name)
                cosmetic_list.append(cosmetic_info)

    return EC_name, name, price

items = []
def get_items_name_from_df(df):
    for goods_index in range(1,len(df.index)):      #取出所有品名
        goods_name = df.at[goods_index, '中文名']
        items.append(goods_name)
    return items

items_momo=[]
def get_items_name_from_df_for_momo(df):
    for goods_index in range(1,len(df.index)):      #取出所有品名
        goods_name = df.at[goods_index, '中文名']
        if "01" in goods_name or "02" in goods_name or "03" in goods_name or "04" in goods_name or "05" in goods_name or "06" in goods_name or "07" in goods_name or "08" in goods_name or "09" in goods_name or "10" in goods_name or "11" in goods_name or "12" in goods_name or "13" in goods_name or "14" in goods_name or "15" in goods_name or "自然色" in goods_name or "明亮色" in goods_name or " 1" in goods_name or " 2" in goods_name:
            items_momo.append(goods_name[0:-7])
        else:
            items_momo.append(goods_name)
    return items_momo

try:
    get_items_name_from_df(df)
    for item_index, item_name in enumerate(items, start=1):
        for ec in ECs:
            url = get_url_by_goods_name(item_name, ec)
            EC_name, name, price = get_goods_info(url)
            df.at[item_index, ec] = price
            print(name, EC_name, price)
    get_items_name_from_df_for_momo(df)
    for item_index, item_name in enumerate(items_momo, start=1):
        url = get_momo_url_by_goods_name(item_name)
        EC_name, name, price = get_goods_info(url)
        df.at[item_index, 'MOMO'] = price
        print(name, EC_name, price)

finally:
    driver.close()

print(df)
