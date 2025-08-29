from peewee import IntegrityError
from telebot import TeleBot
from telebot.types import Message, BotCommand
from states import reg_states
from keyboards.keybords import choise_lang_markup, back_to_choise, first_step_markup, commands
from services.get_data import get_data
from database.peewee_db import User, History, create_models


def reg_handlers(bot: TeleBot):
    bot.set_my_commands([
        BotCommand("/start", "Запустить бота"),
        BotCommand("/help", "Помощь и команды"),
        BotCommand("/history", "Посмотреть историю запросов")
    ])

    create_models()

    @bot.message_handler(commands=['help'])
    def show_cmd(message: Message):
        cmds = bot.get_my_commands()
        output_txt = 'Доступные команды: \n\n'

        for cmd in cmds:
            output_txt += f'{cmd.command} - {cmd.description}\n'
        bot.send_message(message.chat.id, output_txt, reply_markup=commands())
        bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)


    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        try:
            User.create(
                user_id = user_id,
                user_name = username,
                first_name = first_name
            )
            bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!\n"
                                              "Этот бот поможет тебе перевести необходимые слова, "
                                              "а также узнать новые синонимы.\n"
                                              "Для выбора нужного словаря воспользуйся кнопками ниже\n", reply_markup=choise_lang_markup())
        except IntegrityError:
            bot.send_message(message.chat.id, f"Рад снова тебя видеть!\n"
                                              "Для выбора нужного словаря воспользуйся кнопками ниже\n", reply_markup=choise_lang_markup())
        bot.set_state(message.from_user.id, reg_states.choise, message.chat.id)

    @bot.message_handler(commands=['history'])
    def get_history(message: Message):
        inst = User.get(User.user_id == message.from_user.id)
        data_list = inst.histories
        print(type(data_list))
        output_data = 'Вот история запросов на перевод: \n\n'
        for i_index, i_req in enumerate(data_list):
            output_data += f'{i_index + 1}) {i_req}\n'
        bot.send_message(message.chat.id, output_data, reply_markup=commands(), parse_mode='HTML')
        bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)



    @bot.message_handler(state=reg_states.choise)
    def send_welcome(message: Message):
        bot.set_state(message.from_user.id, reg_states.in_dict, message.chat.id)
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
        if message.text == 'Главное меню':
            bot.set_state(message.from_user.id, reg_states.menu, message.chat.id)
            bot.send_message(message.chat.id, 'Выбери действие', reply_markup=commands())
        else:
            bot.send_message(message.chat.id, f'Отлично! Ты выбрал <b>{message.text}</b>.\n'
                                           f'Пришли любое слово на исходном языке и '
                                           f'я покажу тебе информацию о нем.\n'
                                          f'Если хочешь вернуться к выбору словарей — '
                                          f'нажми на кнопку <b>Вернуться к выбору словарей</b>', reply_markup=back_to_choise(), parse_mode='HTML')

    @bot.message_handler(state=reg_states.in_dict)
    def translate(message: Message):
        if message.text == 'Вернуться к выбору словарей':
            bot.set_state(message.from_user.id, reg_states.choise, message.chat.id)
            bot.send_message(message.chat.id, 'Выбери словарь', reply_markup=choise_lang_markup())
        elif message.text.isalpha() and message.text != 'Вернуться к выбору словарей':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                curr_lang = data.get('lang', 'en-ru')
                result = get_data(message.text, curr_lang)
            cur_user = User.get_or_none(User.user_id == message.from_user.id)
            History.create(
                user = cur_user,
                results = result
            )

            bot.send_message(message.chat.id, f'{result}\n'
                                              f'Если хочешь продолжить — отправь новое слово,\n'
                                              f'Если хочешь вернуться к выбору словарей — '
                                              f'нажми на кнопку <b>Вернуться к выбору словарей</b>', reply_markup=back_to_choise(), parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Слово должно состоять только из букв. Введи корректное слово.', reply_markup=back_to_choise())

    @bot.message_handler(state=None, func=lambda message: True)
    def first_step(message: Message):
        bot.send_message(message.chat.id, 'Чтобы начать — введите /help', reply_markup=first_step_markup())
