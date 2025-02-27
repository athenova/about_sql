import os
import telebot
import json
import glob
import schedule
import time

from datetime import date
from datetime import timedelta
from helpers.textes import gen_text
from helpers.images import gen_image

BOT_TOKEN_NAME = "ATHE_BOT_TOKEN"
BOT_TOKEN = os.environ.get(BOT_TOKEN_NAME)
CHAT_ID = '@about_sql'

def job(CHAT_ID=CHAT_ID, image_gen=False, text_gen=False, problem=True, offset = 0):
    check_date = date.today() + timedelta(days=offset)
    tasks = json.load(open('files/in_progress.json', 'rt', encoding='UTF-8'))
    for task in tasks:
        if task["date"] == check_date.strftime('%Y-%m-%d'):
            folder_name = glob.escape(f"files/data/{task['group'].replace('/', ',')}/{task['name'].replace('/', ',')}")
            
            type = "description" if problem else "solution"
            text_file_name = f"{folder_name}/{type}.txt"
            image_file_name = f"{folder_name}/{type}.png"

            if image_gen: gen_image(task, problem)
            if text_gen: gen_text(task, problem)

            bot = telebot.TeleBot(BOT_TOKEN)

            if os.path.exists(text_file_name):
                bot.send_photo(chat_id=CHAT_ID, photo=open(image_file_name, 'rb'), parse_mode="Markdown", disable_notification=True)

            if os.path.exists(text_file_name):
                bot.send_message(chat_id=CHAT_ID, text=open(text_file_name, 'rt', encoding='UTF-8').read(), parse_mode="Markdown")

if __name__ == '__main__':
    schedule.every().day.at("08:00",'Europe/Moscow').do(job, problem=True)
    schedule.every().day.at("12:00",'Europe/Moscow').do(job, problem=False)

    half_day = 12 * 60 * 60

    for i in range(half_day):
        schedule.run_pending()
        time.sleep(1)
