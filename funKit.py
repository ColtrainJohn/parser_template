# standart
from pathlib import Path


# special
from fp.fp import FreeProxy
import requests


# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# this!
import config




# def get_driver(proxy=False):

#     capabilities = webdriver.DesiredCapabilities.FIREFOX
#     capabilities['marionette'] = True
#     capabilities["pageLoadStrategy"] = "eager"
    
#     if proxy:

#         proxy_address = FreeProxy(country_id=['BR']).get().split('//')[-1]

#         capabilities['proxy'] = {
#             "proxyType": "MANUAL",
#             "httpProxy": proxy_address,
#         }

#     executable_path = str(Path(__file__).absolute().parent) + "/geckodriver"

#     service = Service(executable_path)
#     options = Options()
#     options.add_argument('--log-level=3')
#     options.page_load_strategy = 'eager'
        
#     driver = webdriver.Firefox(
#         service=service,
#         options=options,
#         capabilities=capabilities,
#     )

#     return driver


def get_driver(proxy, remote):

    executable_path = str(Path(__file__).absolute().parent) + "/chromedriver"

    service = Service(executable_path)


    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'

    if proxy:
        options.add_argument('--proxy-server=%s' % FreeProxy(country_id=['BR']).get().split('//')[-1])

    if remote:
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
    driver = webdriver.Chrome(
        service=service,
        options=options,
    )

    return driver


def login(driver):
    try:
        driver.get(config.login_url)
        driver.find_element(By.XPATH, '//input[@id="username"]').send_keys(config.login)
        driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(config.passwd)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        return True

    except:
        return False


def check_driver_proxy(driver):
    
    driver.get('http://www.whatismyproxy.com/')
    proxy_check = driver.find_element(By.XPATH, '//div[@class="information"]')
    
    return proxy_check.text
        

def message_to_telegram(text, chat_id="880726373"):
    response = requests.get(
        f"https://api.telegram.org/bot{config.quequer}/sendMessage?chat_id={chat_id}&text={text}"
    )
    return response.json()


def get_updates(token):
    response = requests.get(
        f"https://api.telegram.org/bot{token}/getUpdates"
    )
    return response.json()
