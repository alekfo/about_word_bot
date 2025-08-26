from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def start_gen_markup():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"Русско-английский словарь")
    button_2 = KeyboardButton(text=r"Англо-русский словарь")

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1, button_2)
    return keyboard

def back_to_menu():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"Вернуться к выбору словарей")

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

# def wait_for_new():
#     # Создаём объекты кнопок.
#     button_1 = KeyboardButton(text=r"Продолжить")
#     button_2 = KeyboardButton(text=r"Вернуться к выбору словарей")
#
#     # Создаём объект клавиатуры, добавляя в него кнопки.
#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(button_1, button_2)
#     return keyboard