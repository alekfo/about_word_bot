from telebot import TeleBot
import random
import os
import time
from database.peewee_db import User, History
from config import ADMIN_ID
from services.get_data import get_data

def get_random_word(lang) -> str:
    base_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(base_path)
    print(lang)
    if lang == "ru":
        file_path = os.path.join(folder_path, 'rus_words_for_mailing.txt')
    elif lang == "en":
        file_path = os.path.join(folder_path, 'eng_words_for_mailing.txt')
    else:
        raise TypeError('В базе данных нет такого списка слов')
    with open(file_path, 'r', encoding='UTF-8') as f:
        words_list = f.read().split('\n')
    return random.choice(words_list)

def daily_mailing(bot: TeleBot):
    while True:
        try:
            users_for_mailing = list(User.select().where(User.mailing_flag == True))
            if users_for_mailing:
                for i_user in users_for_mailing:
                    lang = i_user.lang_for_mailing
                    lang_to_take_word = lang.split('-')[0]
                    word = get_random_word(lang_to_take_word)

                    translate_result = get_data(word, lang)

                    bot.send_message(i_user.user_id, f'Ежедневная порция слов🔔\n\nСлово дня: <b>{word}</b>\n\n{translate_result}',
                                     parse_mode='HTML')
            time.sleep(60)
        except Exception as e:
            bot.send_message(ADMIN_ID, f'Произошла ошибка при массовой рассылке: {e}')
            time.sleep(100)