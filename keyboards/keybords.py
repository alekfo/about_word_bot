from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def choise_lang_markup():
    # Создаём объекты кнопок.
    buttons = [
        r"🇷🇺➡️🇺🇸Русско-английский словарь",
        r"🇺🇸➡️🇷🇺Англо-русский словарь",
        r"🇷🇺➡️🇩🇪Русско-немецкий словарь",
        r"🇷🇺➡️🇫🇷Русско-французский словарь",
        r"🇷🇺🔁🇷🇺Русские синонимы",
        r"🇺🇸🔁🇺🇸Английские синонимы",
        r"↩️Главное меню",
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def back_to_choise():
    # Создаём объекты кнопок.
    button_1 = KeyboardButton(text=r"↩️Вернуться к выбору словарей")

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
    """
        Функция дял создания объекта клавиатуры с кнопками основного меню
        :return: keyboard
        """

    # Создаём объекты кнопок.
    buttons = [
        r"/start",
        r"/help",
        r"/history",
        r"/mailing"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def turning_on_mailing():
    # Создаём объекты кнопок.
    buttons = [
        r"✅Включить ежедневную рассылку",
        r"↩️Главное меню"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard

def turning_off_mailing():
    # Создаём объекты кнопок.
    buttons = [
        r"🚫Выключить ежедневную рассылку",
        r"↩️Главное меню"
    ]

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        keyboard.add(KeyboardButton(text=button_text))
    return keyboard
