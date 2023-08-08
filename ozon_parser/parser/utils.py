from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from ozon_parser.settings import BASE_DIR
import os
from django.http import HttpResponse

from .models import Product

driver_path = os.path.join(BASE_DIR, "drivers/chromedriver")
url = "https://www.ozon.ru/seller/1/products"
domain = "https://www.ozon.ru"
page_load_strategy = "normal"
user_agent = "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"


def get_products(num_of_products: int = 10):
    print("Parsing..")
    options = webdriver.ChromeOptions()
    options.page_load_strategy = page_load_strategy
    options.add_argument(user_agent)
    options.add_argument("--headless")
    driver_service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(options=options, service=driver_service)
    driver.get(url)
    sleep(5)

    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    search_result = bs.find("div", attrs={"class": "widget-search-result-container"})
    res = BeautifulSoup(str(search_result), "html.parser")
    products = res.find_all("a")
    next_page = None
    next = bs.find_all("div", string="Дальше", limit=3)
    for i in next:
        if i.a["href"]:
            next_page = domain + i.a["href"]
            break

    if num_of_products > 36 and next_page:
        driver = webdriver.Chrome(options=options, service=driver_service)
        driver.get(next_page)
        sleep(5)

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        search_result = bs.find(
            "div", attrs={"class": "widget-search-result-container"}
        )
        res = BeautifulSoup(str(search_result), "html.parser")
        another_products = res.find_all("a")
        products = products + another_products
    driver.close()
    driver.quit()
    return products


def save_product(products, num_of_products):
    for item in range(1, num_of_products * 2, 2):
        link = products[item].get("href")
        name = products[item].find("span").get_text()
        product_link = domain + link
        Product.objects.create(name=name, link=product_link)
        sleep(2)
    return HttpResponse("Created")
