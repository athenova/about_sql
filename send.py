from project import Project
import schedule
import time


if __name__ == '__main__':
    p = Project()
    schedule.every().day.at("08:00",'Europe/Moscow').do(p, type='description')
    schedule.every().day.at("12:00",'Europe/Moscow').do(p, type='solution')

    half_day = 12 * 60 * 60

    for i in range(half_day):
        schedule.run_pending()
        time.sleep(1)
