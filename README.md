Простой Telegram Bot для доступа к функционалу ChatGPT посредством Telegram, написанный на Python.

## Подготовка

> Инструкция ниже написана для Debian-подобных систем.

- Установите Tesseract-OCR на свой хост:

```bash
sudo apt install tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng  
```

- Установите ffmpeg на свой хост:

```bash
sudo apt install ffmpeg
```

- Установите все необходимые библиотеки для Python:

```bash
pip3 install -r requirements.txt
```

- Укажите свои переменные окружения для использования бота:

`env.env:`
```bash
TELEGRAM_BOT_API_KEY=<telegram_bot_api_key>
OPENAI_API_KEY=<openai_api_key>
ALLOWED_USERS_ID=<user_id_1>,<user_id_2>,<user_id_3>
```

> Формат ID пользователей: _123456789_.

## Использование

- Запустите файл `run.py`:

```bash
python run.py
```

## Telegram Bot API

Для создания этого бота была задействована библиотека pyTelegramBotAPI. Больше информации вы найдете здесь:Для создания
этого бота была задействована библиотека pyTelegramBotAPI. Больше информации вы найдете
здесь:[клик](https://github.com/eternnoir/pyTelegramBotAPI)
