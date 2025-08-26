from telebot import TeleBot
from telebot.types import Message
from states import reg_states
from keyboards.keybords import start_gen_markup, back_to_menu
from services.get_data import get_data


def reg_handlers(bot: TeleBot):

    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        bot.set_state(message.from_user.id, reg_states.choise, message.chat.id)
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!\n"
                                          "Этот бот поможет тебе перевести необходимые слова,"
                                          "а также узнать узнать новые синонимы\n"
                                          "Для выбора нужного словаря воспользуйся копками ниже\n", reply_markup=start_gen_markup())

    @bot.message_handler(state=reg_states.choise)
    def send_welcome(message: Message):
        bot.set_state(message.from_user.id, reg_states.in_dict, message.chat.id)
        bot.send_message(message.chat.id, f'Отлично! Ты выбрал {message.text}.\n'
                                           f'Отправь любое слово на исходном языке и'
                                           f'я пришлю тебе информацию о нем'
                                          f'Если хочешь вернуться к выбору словарей'
                                          f'нажми на кнопку "Вернуться к выбору словарей"', reply_markup=back_to_menu())

    @bot.message_handler(state=reg_states.in_dict)
    def translate(message: Message):
        if message.text.isalpha() and message.text != 'Вернуться к выбору словарей':
            result = get_data(message.text)
            bot.send_message(message.chat.id, f'{result}\n'
                                              f'Если хотите продолжить - отправьте новое слово,\n'
                                              f'Если хочешь вернуться к выбору словарей'
                                              f'нажми на кнопку "Вернуться к выбору словарей"', reply_markup=back_to_menu())
        elif message.text == 'Вернуться к выбору словарей':
            bot.set_state(message.from_user.id, reg_states.choise, message.chat.id)
            bot.send_message(message.chat.id, 'Выбери словарь', reply_markup=start_gen_markup())

    @bot.message_handler(state=None, func=lambda message: True)
    def first_step(message: Message):
        bot.send_message(message.chat.id, 'Чтобы начать - введите /start')
