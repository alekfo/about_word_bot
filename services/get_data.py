import requests
import json
import config
from typing import Any


def get_data(word, lang):
    """
    Функция для работы с API Yandex
    :param word: строка со словом от пользователя
    :param lang: направление перевода
    :return: запрашивает данные по заданному URL, парсит данные
     в нужный формат для вывода, возвращает строку с информацией
     о слове в соответствии с навпрвлением перевода
    """

    base_url = config.APP_URL

    app_key = config.APP_KEY

    params = {
        'key': app_key,
        'lang': lang,  # Направление перевода
        'text': word,  # Слово для перевода
        'ui': 'ru'  # Хотим получать пояснения на русском
    }

    if lang in ['ru-ru', 'en-en']:
        mode = 'синонимы'
    else:
        mode = 'переводы'

    response = requests.get(base_url, params).json()
    if not response['def']:
        return f'По твоему запросу ничего не найдено\n'

    data = {}

    for i_speech in response['def']:
        definitions = []
        for i_def in i_speech['tr']:
            definitions.append(i_def['text'])
        data[i_speech['pos']] = definitions

    output_str = f'Направление перевода: <b>{lang}</b>\nНайденные {mode} слова <b>{word.upper()}</b>:\n'
    for i_key, i_val in data.items():
        output_str += f'<b>{i_key.upper()}</b>: {', '.join(i_val)}\n'

    return output_str