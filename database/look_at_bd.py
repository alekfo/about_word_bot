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

# username_to_delete = "alek_fo"
# deleted_count = User.delete().where(User.user_name == username_to_delete).execute()
# username_to_delete = "pinkiss7"
# deleted_count = User.delete().where(User.user_name == username_to_delete).execute()

clients = list(User.select())

for i_user in clients:
    print(i_user.user_name)
    print(i_user.mailing_flag)