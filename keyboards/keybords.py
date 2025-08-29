from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def choise_lang_markup():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"Русско-английский словарь")
    button_2 = KeyboardButton(text=r"Англо-русский словарь")
    button_3 = KeyboardButton(text=r"Русско-немецкий словарь")
    button_4 = KeyboardButton(text=r"Русско-французский словарь")
    button_5 = KeyboardButton(text=r"Русские синонимы")
    button_6 = KeyboardButton(text=r"Английские синонимы")
    button_7 = KeyboardButton(text=r"Главное меню")


    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7)
    return keyboard

def back_to_choise():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"Вернуться к выбору словарей")

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

def first_step_markup():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"/help")

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    return keyboard

def commands():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"/start")
    button_2 = KeyboardButton(text=r"/help")
    button_3 = KeyboardButton(text=r"/history")

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1, button_2, button_3)
    return keyboard