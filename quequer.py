# standart libs
import warnings
from time import sleep

# special libs
from loguru import logger
from pandas import to_datetime

# selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# this lib
import config
import funKit


warnings.filterwarnings("ignore", category=DeprecationWarning)


class Bot:

    def __init__(self, service='Perfectarea actelor notariale'):

        self.service = service
        
        self.driver = funKit.get_driver(proxy=True)
        self.driver.implicitly_wait(10)
        
        self.avaliable_visit_time = dict()
        
        logger.info(
            f'Got proxy address: {self.driver.capabilities["proxy"]["httpProxy"]}'
        )


    def workflow(self):

        if funKit.login(self.driver):

            sleep(5)
            self.go_to_services_page()
            self.choose_service()

            if self.are_there_available_dates():

                self.some_clicks()
                self.parse_nearest_months('2023-02-23')
                self.confirm()

            else:
                
                logger.info("There are no avaiable dates")
                funKit.message_to_telegram("There are no avaiable dates")


    def go_to_services_page(self):
        try:
            self.driver.get('https://ambasada-r-moldova-in-f-rusa.reservio.com/services')
            
        except Exception as err:
            funKit.message_to_telegram("Services page error: " + str(err))


    def choose_service(self):
        try:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, self.service).click()

        except Exception as err:
            funKit.message_to_telegram("Service choose error: " + str(err))


    def are_there_available_dates(self):
        if EC.visibility_of((By.XPATH, "//div[contains(@class, 'calendarHeader')]")):
            return True
        return False


    def some_clicks(self):
        try:
            self.driver.find_element(By.XPATH, '//a[@data-test="link-service-detail-page-book-now"]').click()
        except:
            pass

        try:
            self.driver.find_element(By.XPATH, '//span[text()="Anyone available"]').click()
        except:
            pass

    
    def parse_nearest_months(self, date):
        
        for should_turn_the_page in range(3):

            if should_turn_the_page:
                self.driver.find_element(By.XPATH, '//button[@aria-label="Next month"]').click()

            month_and_year = self.driver.find_element(By.XPATH, '//div[starts-with(@class, "calendarHeader-")]').text
            month, year = month_and_year.split()
            month = config.monthToDigit[month.capitalize()]

            available_dates = self.driver.find_elements(
                By.XPATH, "//button[starts-with(@class, 'dayCell') and not(@disabled = '')]"
            )  
            
            for day in available_dates:
                
                day.click()
                available_time = self.driver.find_elements(
                    By.XPATH, '//div[contains(@data-test, "btn-booking-flow-service-choose-term-booking-slots-chip")]'
                )

                for time in available_time:

                    self.avaliable_visit_time.update({
                        to_datetime('-'.join([year, month, day.text]) + ' ' + time.text) : time
                    })

                    if to_datetime('-'.join([year, month, day.text]) + ' ' + time.text) >= to_datetime(date):
                        time.click()
                        return True

        return False


    def confirm(self):
        self.driver.find_elements(By.XPATH, '//button[@data-test="link-booking-flow-proceed-to-checkout"]')[1].click()
        #self.driver.find_element(By.XPATH, '//input[@data-test="checkbox-booking-flow-consent-business-pp-box"]').click()
        self.driver.find_element(By.XPATH, '//button[@data-test="btn-booking-flow-booking-details-confirm-and-pay"]').click()







def main():

    bot = Bot()

    try:
        bot.workflow()
        

    except Exception as err:
        logger.info(err)

    finally:
        sleep(5)
        bot.driver.close()
        bot.driver.quit()



if __name__ == '__main__':
    main()