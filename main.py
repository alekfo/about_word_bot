import telebot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
import threading

from config import BOT_TOKEN
from database.peewee_db import create_models

from handlers.main_handlers import reg_main_handlers
from handlers.in_dict_handlers import reg_in_dict_handlers
from handlers.сancel_handler import reg_cancel_handlers
from handlers.menage_daily_mailing import reg_daily_mailing_handlers
from handlers.any_message_handler import any_message_handlers

from utils.words_daily_mailing import daily_mailing




def main():
    """
    Основная функция для запуска бесконечного цикла взаимодействия с API
    сервера телеграма.
    Переменной bot присваивается объект класса TeleBot.
    Переменная bot регистрирует все возможные сценарии полученных сообщений
    в функции reg_handlers.
    С помощью bot.infinity_polling() запускается бесконечный цикл опроса API
    телеграма
    """

    create_models()
    state_storage = StateMemoryStorage()

    bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)
    bot.add_custom_filter(custom_filters.StateFilter(bot))

    reg_cancel_handlers(bot)
    reg_main_handlers(bot)
    reg_in_dict_handlers(bot)
    reg_daily_mailing_handlers(bot)
    any_message_handlers(bot)

    # Запускаем поток для проверки уведомлений
    notification_thread = threading.Thread(
        target=daily_mailing,
        args=(bot,),
        daemon=True  # Поток завершится при завершении основного потока
    )
    notification_thread.start()

    bot.infinity_polling()

if __name__ == '__main__':
    main()