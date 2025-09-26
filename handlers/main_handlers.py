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


def reg_main_handlers(bot: TeleBot):
    """
    Функция регистрации основных обработчиков в bot
    :param bot: объект бота (объект класса TeleBot)
    :return: None. Изменяется состояние объекта бота
    Все возможные сценарии полученных сообщений регистрируются в объект бота с помощью декораторов
    """

    bot.set_my_commands([
        BotCommand("/start", "🌐Запустить переводчик"),
        BotCommand("/help", "ℹ️Помощь и команды"),
        BotCommand("/history", "📖Посмотреть историю запросов"),
        BotCommand("/mailing", "🔔Управлять ежедневной рассылкой")
    ])


    @bot.message_handler(commands=['help'])
    def show_cmd(message: Message):
        """
        Обработчик команды /help
        :param message: сообщение от пользователя
        После обработки отправляет пользователю сообщение с доступными командами и
        клавиатурой с доступными командами, меняет статус данного пользователя на menu
        """

        curr_user = User.get_or_none(User.user_id == message.from_user.id)
        if curr_user:
            cmds = bot.get_my_commands()
            output_txt = 'Доступные команды: \n\n'

            for cmd in cmds:
                output_txt += f'{cmd.command} - {cmd.description}\n'
            bot.send_message(message.chat.id, output_txt, reply_markup=commands())
            bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Похоже ты тут впервые? Чтобы понять что к чему нажми на /start', reply_markup=commands(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)

    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        """
        Обработчик команды /start
        :param message: сообщение от пользователя
        После обработки отправляет пользователю приветственное сообщение
        с клавиатурой возможных направлений перевода,
        меняет состояние на choise
        """

        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        try:
            User.create(
                user_id = user_id,
                user_name = username,
                first_name = first_name,
                lang_for_mailing = 'ru-en'
            )
            bot.send_message(message.chat.id, f"👋Привет, {message.from_user.first_name}!\n"
                                              "Этот бот поможет тебе перевести необходимые слова, "
                                              "а также узнать новые синонимы.\n"
                                              "🌐Для выбора нужного словаря воспользуйся кнопками ниже\n\n"
                                              "↩️Для перехода в основное меню нажмите на кнопку <b>Главное меню</b>", reply_markup=choise_lang_markup(), parse_mode='HTML')
        except IntegrityError:
            bot.send_message(message.chat.id, f"👋Рад снова тебя видеть!\n"
                                              "🌐Для выбора нужного словаря воспользуйся кнопками ниже\n\n"
                                              "↩️Для перехода в основное меню нажмите на кнопку <b>Главное меню</b>", reply_markup=choise_lang_markup(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states.choise, message.chat.id)

    @bot.message_handler(commands=['history'])
    def get_history(message: Message):
        """
        Обработчик команды /history
        :param message: сообщение от пользователя
        После обработки отправляет пользователю историю запросов с клавиатурой разделов
        """
        curr_user = User.get_or_none(User.user_id == message.from_user.id)
        if curr_user:
            inst = User.get(User.user_id == message.from_user.id)
            data_list = inst.histories
            last_5_requests = data_list[-5:] if len(data_list) > 5 else data_list
            output_data = '📖Вот история последних 5 запросов на перевод: \n\n'
            for i_index, i_req in enumerate(last_5_requests):
                output_data += f'🈯{i_req}\n'
            bot.send_message(message.chat.id, output_data, reply_markup=commands(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Похоже ты тут впервые? Чтобы понять что к чему нажми на /start', reply_markup=commands(), parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)

    @bot.message_handler(commands=['mailing'])
    def get_mailing(message: Message):
        """
        Обработчик команды /mailing
        :param message: сообщение от пользователя
        """

        curr_user = User.get_or_none(User.user_id == message.from_user.id)
        if curr_user:
            inst = User.get(User.user_id == message.from_user.id)
            if inst.mailing_flag:
                bot.send_message(message.chat.id, '✅Ежедневная рассылка <b>включена</b>.\n'
                                                  'Чтобы выключить ежедневную рассылку нажмите на копку выключения\n'
                                                  '↩️Для возврата в основное меню нажмите на кнопку <b>Главное меню</b>',
                                 reply_markup=turning_off_mailing(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states.in_menage_mailing, message.chat.id)
            else:
                bot.send_message(message.chat.id, '🚫Ежедневная рассылка <b>выключена</b>.\n'
                                                  'Чтобы включить ежедневную рассылку нажмите на копку включения\n'
                                                  '↩️Для возврата в основное меню нажмите на кнопку <b>Главное меню</b>',
                                 reply_markup=turning_on_mailing(), parse_mode='HTML')
                bot.set_state(message.from_user.id, reg_states.in_menage_mailing, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Похоже ты тут впервые? Чтобы понять что к чему нажми на /start', reply_markup=commands(),
                             parse_mode='HTML')
            bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)

