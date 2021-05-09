from dvmn_client import DevmanApi
from constants import DEVMAN_URL
import requests
import os
from pprint import pp
import telegram

if __name__ == '__main__':
    lib = DevmanApi(os.getenv("api_key"))
    bot = telegram.Bot(token=os.getenv("bot_token"))
    while True:
        try:
            res = lib.get_long_polling_reviews(lib.get_timestamp())
            pp(res)
            if res['status'] == 'found':
                last_attempt = [attempt for attempt in res['new_attempts']][-1]
                have_mistakes = "Работа выполнена без ошибок!"
                if last_attempt['is_negative']:
                    have_mistakes = "К сожалению, в работе есть ошибки"
                bot.send_message(chat_id=os.getenv('chat_id'), text="""Преподаватель проверил работу!
                Урок - {lesson}.
                
                {mistakes}
                
                Ссылка на работу - {lesson_url}
                """.format(
                    lesson=last_attempt['lesson_title'],
                    mistakes=have_mistakes,
                    lesson_url=DEVMAN_URL.format(last_attempt['lesson_url'])
                    )
                                 )
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(e)
