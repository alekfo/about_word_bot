import requests
import json
import config
from typing import Any


def get_data(word):
    langs = ['en-ru', 'ru-en', 'ru-de', 'ru-es', 'ru-lv']

    base_url = config.APP_URL

    app_key = config.APP_KEY

    params = {
        'key': app_key,
        'lang': 'en-ru',  # Направление перевода
        'text': word,  # Слово для перевода
        'ui': 'ru'  # Хотим получать пояснения на русском
    }

    response = requests.get(base_url, params).json()

    data = {}

    for i_speech in response['def']:
        definitions = []
        for i_def in i_speech['tr']:
            definitions.append(i_def['text'])
        data[i_speech['pos']] = definitions

    output_str = f'Вот найденные переводы слова {word}\n'
    for i_key, i_val in data.items():
        output_str += f'{i_key}: {', '.join(i_val)}\n'

    return output_str