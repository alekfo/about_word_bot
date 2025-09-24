from peewee import IntegrityError
from telebot import TeleBot
from telebot.types import Message, BotCommand
from states import reg_states
from keyboards.keybords import (choise_lang_markup,
                                back_to_choise,
                                first_step_markup,
                                commands,
                                turning_on_mailing,
                                turning_off_mailing)
from services.get_data import get_data
from database.peewee_db import User, History

def any_message_handlers(bot: TeleBot):
    """
    Функция регистрации обработчика любых сообщений
    :param bot: объект бота (объект класса TeleBot)
    :return: None. Изменяется состояние объекта бота
    """

    @bot.message_handler(state=None, func=lambda message: True)
    def first_step(message: Message):
        """
        Обработчик любого сообщения при условии отсутствия состояния
        :param message: любое сообщение от пользователя, когда еще не задано состояние,
        предполагется в начале диалога.
        Отправляет пользователю сообщение с клавиатурой help
        """

        bot.send_message(message.chat.id, '🚀Чтобы начать — введите /help', reply_markup=first_step_markup())