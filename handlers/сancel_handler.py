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

def reg_cancel_handlers(bot: TeleBot):
    """
    Функция регистрации обработчика для отмены
    :param bot: объект бота (объект класса TeleBot)
    :return: None. Изменяется состояние объекта бота
    Все возможные сценарии полученных сообщений регистрируются в объект бота с помощью декораторов
    """

    @bot.message_handler(state=[reg_states.in_menage_mailing,
                                reg_states.choise,
                                reg_states.complete_setting_mailing],
                         func=lambda message: 'Главное меню' in message.text)
    def return_to_menu(message: Message):
        bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)
        bot.send_message(message.chat.id, 'Выбери действие', reply_markup=commands())