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

def reg_daily_mailing_handlers(bot: TeleBot):
    """
    Функция регистрации основных обработчиков в bot
    :param bot: объект бота (объект класса TeleBot)
    :return: None. Изменяется состояние объекта бота
    Все возможные сценарии полученных сообщений регистрируются в объект бота с помощью декораторов
    """

    @bot.message_handler(state=reg_states.in_menage_mailing)
    def menage_daily_mailing(message: Message):
        """
        Обработчик состояния in_menage_mailing
        :param message: сообщение от пользователя
        """
        try:
            curr_client = User.get_or_none(User.user_id ==message.from_user.id)
            if 'Выключить ежедневную рассылку' in message.text and curr_client.mailing_flag:
                curr_client.mailing_flag = False
                curr_client.save()
                bot.send_message(message.chat.id, '🚫Ежедневная рассылка выключена\n\n'
                                                  '⚙️Выберите действие', reply_markup=commands(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)
            elif 'Включить ежедневную рассылку' in message.text and not curr_client.mailing_flag:
                bot.send_message(message.chat.id, 'Выберите направление словаря для ежедневной рассылки\n'
                                                  '↩️Для возврата в основное меню нажми <b>Главное меню</b>', reply_markup=choise_lang_markup(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states.complete_setting_mailing, message.chat.id)
        except Exception as e:
            bot.send_message(message.chat.id, f'❌Произошла ошибка: {e}\n\n'
                                              '⚙️Выберите действие', reply_markup=commands(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)

    @bot.message_handler(state=reg_states.complete_setting_mailing)
    def menage_daily_mailing(message: Message):
        """
        Обработчик состояния in_menage_mailing
        :param message: сообщение от пользователя
        """
        try:
            curr_client = User.get_or_none(User.user_id == message.from_user.id)
            if 'Русско-английский словарь' in message.text:
                lang = 'ru-en'
            elif 'Англо-русский словарь' in message.text:
                lang = 'en-ru'
            elif 'Русско-немецкий словарь' in message.text:
                lang = 'ru-de'
            elif 'Русско-французский словарь' in message.text:
                lang = 'ru-fr'
            elif 'Русские синонимы' in message.text:
                lang = 'ru-ru'
            elif 'Английские синонимы' in message.text:
                lang = 'en-en'
            else:
                raise ValueError('🚫Такого направления нет в базе данных. Попробуй снова')
            if curr_client.mailing_flag:
                raise ValueError('У пользователя уже включена ежедневная рассылка')
            else:
                curr_client.mailing_flag = True
                curr_client.lang_for_mailing = lang
                curr_client.save()
                bot.send_message(message.chat.id, f'✅Ежедневная рассылка включена. Направление перевода - <b>{lang}</b>\n\n'
                                                  '⚙️Выберите действие', reply_markup=commands(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка: {e}\n\n'
                                              '⚙️Выберите действие', reply_markup=commands(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)
