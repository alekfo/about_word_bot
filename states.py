from telebot.handler_backends import State, StatesGroup

class reg_states(StatesGroup):

    choise = State()
    in_dict = State()
    menu = State()