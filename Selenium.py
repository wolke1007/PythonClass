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
driver.get("https://www.google.com/")


def wait_until(xpath: str):
    element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(("xpath", xpath))
    )
    return element

try:
    search_input_field = wait_until("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
    search_input_field.send_keys("biggo")
    google_search_button = wait_until("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[2]/div[2]/div[5]/center/input[1]")
    google_search_button.click()
    search_result = wait_until('//h3[@class="LC20lb MBeuO DKV0Md"][text()="比個夠BigGo 比價網- 商品價格搜尋引擎"]')
    search_result.click()
    biggo_input = wait_until("/html/body/div[3]/div/div/form/div/input[1]")
    biggo_input.send_keys("CLIO珂莉奧 凝時美肌防沾染柔霧粉底液 精巧版")
    biggo_search_button = wait_until("/html/body/div[3]/div/div/form/div/input[2]")
    biggo_search_button.click()
    EC_select_momo = wait_until("/html/body/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div[1]/div/label/span[2]")
    EC_select_momo.click()
    EC_select_pc24 = wait_until("/html/body/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div[4]/div/label/span[2]")
    EC_select_pc24.click()
    EC_select_book = wait_until("/html/body/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div[3]/div/label/span[2]")
    EC_select_book.click()
    EC_select_cosmed = wait_until("/html/body/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div[6]/div/label/span[2]")
    EC_select_cosmed.click()
    EC_select_watsons = wait_until("/html/body/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div[7]/div/label/span[2]")
    EC_select_watsons.click()
    EC_search_button = wait_until("/html/body/div[3]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div")
    EC_search_button.click()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    response = requests.get(driver.current_url,headers=headers)
    cosmetic_list = []
    soup = BeautifulSoup(response.text, 'lxml')
    info_items = soup.find_all('div', 'col-12 product-row')
    for item in info_items:
        name = item.find('div', 'list-product-name line-clamp-2').a.text.strip()
        price = item.find('div', 'd-flex flex-wrap align-items-center', 'price').a.text.strip()
        EC = item.find('div', 'store-name-wrap', 'store').text.strip()
        cosmetic_info = dict(品名=name, 價格=price, 通路=EC)
        cosmetic_list.append(cosmetic_info)
    #    movie.execute('INSERT INTO MOVIE_INFO VALUES(?,?,?)', (name,english_name,release_time))
    #    conn.commit()
    #    print('{}({}) 上映日：{}'.format(name, english_name, release_time))

    print(cosmetic_list)
finally:
    print("Done")
