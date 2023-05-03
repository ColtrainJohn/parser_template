# standart libs
import warnings
from time import sleep


# special libs
#from loguru import logger


# selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# this lib
import config
import funKit



class Bot:

    def __init__(self, proxy=False, remote=False, service=False):

        self.service = service
        
        self.driver = funKit.get_driver(proxy=proxy, remote=remote)
        self.driver.implicitly_wait(10)


    def login(self):

        try:
            self.driver.get(config.login_url)
            self.driver.find_element(By.XPATH, '//input[@id="username"]').send_keys(config.login)
            sleep(2)
            self.driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(config.passwd)
            sleep(1)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            return True

        except:
            return False


    def go_to_services_page(self):
        sleep(5)
        try:
            # self.driver.find_element(By.XPATH, "//a[contains(@data-test, 'visited-businesses')]").click()
            self.driver.get(config.services_url)
            
        except Exception as err:
            funKit.message_to_telegram("Services page error: " + str(err))


    def choose_service(self):
        try:
            # self.driver.find_element(By.PARTIAL_LINK_TEXT, self.service).click()
             self.driver.find_element(By.XPATH, "//li[contains(@class, 'serviceBookRow')][1]//div[contains(@class, 'rightContent')]").click()

        except Exception as err:
            funKit.message_to_telegram("Service choose error:\n" + str(err))


    def check_staff_if_necessary(self):
        h1 = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'root')]")
        header = h1.get_attribute('textContent')

        if header == "Choose a staff member":
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Anyone available").click()



    def there_are_available_dates(self):

        try:
            self.driver.find_element(By.XPATH, "//div[contains(@class, 'calendarHeader')]")
            for _ in range(30):
                funKit.message_to_telegram("Чекни сайт", chat_id='-952092728')
                sleep(1)
            return True

        except NoSuchElementException:

            funKit.message_to_telegram("No available dates", chat_id='880726373')
            return False


def main():

    bot = Bot(service='Perfectare buletinului', remote=True)

    try:
        bot.login()
        bot.go_to_services_page()
        sleep(5)
        bot.choose_service()
        sleep(5)
        bot.check_staff_if_necessary()
        sleep(5)
        bot.there_are_available_dates()
        

    except Exception as err:
        #logger.info(err)
        pass

    finally:
        sleep(5)
        bot.driver.close()
        bot.driver.quit()



if __name__ == '__main__':
    main()

