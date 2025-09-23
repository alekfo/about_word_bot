from peewee import IntegrityError
from telebot import TeleBot
from telebot.types import Message, BotCommand
from states import reg_states
from keyboards.keybords import choise_lang_markup, back_to_choise, first_step_markup, commands
from services.get_data import get_data
from database.peewee_db import User, History

def reg_in_dict_handlers(bot: TeleBot):
    """
    Функция регистрации всех возможных обработчиков в bot
    :param bot: объект бота (объект класса TeleBot)
    :return: None. Изменяется состояние объекта бота
    Все возможные сценарии полученных сообщений регистрируются в объект бота с помощью декораторов
    """

    @bot.message_handler(state=reg_states.choise)
    def send_welcome(message: Message):
        """
        Обработчик состояния choise (ловит это состояние)
        :param message: сообщение от пользователя c выбранным направлением перевода
        После обработки отправляет пользователю сообщение с выбранным направлением перевода,
        предлагает пользователю отправить слово для перевода,
        также содержит клавиатуру для возврата к выбору словарей.
        При получении текста "Главное меню" меняет состояние на menu и
        отправляет клавиатуру с основными командами.
        Меняет состояние на in_dict
        """

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if message.text == 'Русско-английский словарь':
                data['lang'] = 'ru-en'
            elif message.text == 'Англо-русский словарь':
                data['lang'] = 'en-ru'
            elif message.text == 'Русско-немецкий словарь':
                data['lang'] = 'ru-de'
            elif message.text == 'Русско-французский словарь':
                data['lang'] = 'ru-fr'
            elif message.text == 'Русские синонимы':
                data['lang'] = 'ru-ru'
            elif message.text == 'Английские синонимы':
                data['lang'] = 'en-en'

        bot.send_message(message.chat.id, f'Отлично! Ты выбрал <b>{message.text}</b>.\n'
                                          f'Пришли любое слово на исходном языке и '
                                          f'я покажу тебе информацию о нем.\n'
                                          f'Если хочешь вернуться к выбору словарей — '
                                          f'нажми на кнопку <b>Вернуться к выбору словарей</b>',
                         reply_markup=back_to_choise(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states.in_dict, message.chat.id)

    @bot.message_handler(state=reg_states.in_dict)
    def translate(message: Message):
        """
        Обработчки состояния in_dict (ловит слова для перевода)
        :param message: сообщение от пользователя c
        словом для перевода или сообщением "Вернуться к выбору словарей".
        При получении 'Вернуться к выбору словарей' меняет состояние на choise и
        отправляет клавиатуру для выбора слоаварей.
        При получении слова для перевода делает запрос к функции get_data для получения информации
        о данном слова.
        Записывает в модель History базы данных полученные данные от get_data.
        Отправляет пользователю строку с информацией о слове
        """

        if message.text == 'Вернуться к выбору словарей':
            bot.set_state(message.from_user.id, reg_states.choise, message.chat.id)
            bot.send_message(message.chat.id, 'Выбери словарь', reply_markup=choise_lang_markup())
        elif message.text.isalpha() and message.text != 'Вернуться к выбору словарей':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                curr_lang = data.get('lang', 'en-ru')
                result = get_data(message.text, curr_lang)
            cur_user = User.get_or_none(User.user_id == message.from_user.id)
            History.create(
                user=cur_user,
                results=result
            )

            bot.send_message(message.chat.id, f'{result}\n'
                                              f'Если хочешь продолжить — отправь новое слово,\n'
                                              f'Если хочешь вернуться к выбору словарей — '
                                              f'нажми на кнопку <b>Вернуться к выбору словарей</b>',
                             reply_markup=back_to_choise(), parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Слово должно состоять только из букв. Введи корректное слово '
                                              'или вернись к выбору словарей, нажав на кнопку.',
                             reply_markup=back_to_choise())