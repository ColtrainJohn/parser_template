import schedule
import time

from quequer import main


if __name__ == '__main__':
    
    schedule.every().hour.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)