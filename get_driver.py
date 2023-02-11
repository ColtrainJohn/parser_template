from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config import driverOptions


def getDriver(driverOptions=[]):

    executable_path = str(Path(__file__).absolute().parent) + "/chromedriver"

    service = Service(executable_path)

    options = Options()
    for option in driverOptions:
        options.add_argument(option)

    driver = webdriver.Chrome(
        service=service,
        options=options,
    )

    return driver

if __name__ == '__main__':
    
    driver = getDriver(driverOptions)
    
    try:
        driver.get('https://en.wikipedia.org/wiki/Entropy')

        print(
            driver.find_element(
                By.XPATH, "/html/head/title").get_attribute("innerHTML")
            )
        sleep(10)

    except Exception as err:
        print(err)

    finally:
        driver.close()
        driver.quit()