# Название прокта
Сервис "Учим слова"
🤖 Telegram-bot: @about_word_bot

 [Свяжитесь с нашим ботом:](https://t.me/about_word_bot)

 Ссылка на репозиторий: https://github.com/alekfo/about_word_bot

# Описание прокта
Telegram-бот для перевода слов между языками с 
использованием API Yandex Словаря.

# Возможности

- 🔍 Пользовательский выбор языка
- 🌍 Доступные направления перевода:
  - русско-английский словарь
  - англо-русский словарь
  - русско-немецкий словарь
  - русско-францусский словарь
  - словарь русских синонимов
  - словарь английских синонимов
- ⚡ Быстрый ответ через Yandex API
- 🔔Функция ежедневной рассылки слов (можно выключить)
- 📱 Удобный интерфейс в Telegram
- 🎯 Поддержка команд для смены языка перевода
- 💾 возможность просмотра истории запросов 

# Основные технологии
## Python
```
Использумые библиотеки в файле requirements.txt
База данных: ORM Peewee
Библиотека для телеграм: telebot
```

## Docker
Сборка образа и запуск контейнера описаны ниже

# Установка и запуск

### Клонирование репозитория
```markdown
bash
git clone https://github.com/alekfo/about_word_bot.git
cd about_word_bot
```

### Установка зависимостей
```markdown
bash
pip install -r requirements.txt
```
### Настройка переменных окружения
Создайте файл .env и добавьте:

BOT_TOKEN=YOUR_TOKEN

YANDEX_KEY=YOUR_YA_KEY

YANDEX_URL=YOUR_BASE_URL

DB_PATH=YOUR_DB_PATH

ADMIN_ID=YOUR_ID


### Запуск проекта через терминал
```markdown
bash
python main.py
```

### Сборка контейнера Docker
В проекте уже собраны Dockerfile и docker-compose.yml. Для сборки образа docker и запуска контейнера необходимо указать путь до файла с базой данных
на вашем локальном устройстве заменив строку '- "/home/vboxuser/PycharmProjects/about_word_bot/DATABASE:/app/data"' на ваш путь.
Для сборки образа и запуска контейнера:
```
bash
cd about_word_bot
docker compose up -d
```

# Использование
Для запуска дилога с ботом достаточно отправить любое сообщение
### Основные команды
    - /start - запуск основного меню со словарями
    - /help - просмотр доступных команд
    - /history - просмотр истории запросов
    - /mailing - управлять ежедневной рассылкой
### Пример использования:
1. [Основное меню](screenshots\main_menu.png)
2. [Режим переводчика](screenshots\translator_mode.png)
3. [Пример перевода слова](screenshots\translate_example.png)
4. [Вывод истории запросов](screenshots\history.png)
5. [Управление ежедневной рассылкой](screenshots\daily_mailing_manage.png)
7. [Пример полученного "Слова дня""](screenshots\daily_mailing.png)

# Автор
Шленсков Алексей



