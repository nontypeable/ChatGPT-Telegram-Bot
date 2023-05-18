Простой Telegram Bot для доступа к функционалу ChatGPT посредством Telegram, написанный на Python.

## Подготовка

> Инструкция ниже написана для Debian.

- Установите Tesseract-OCR на свой сервер:

```bash
sudo apt install tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng  
```

- Установите ffmpeg на свой сервер:

```bash
sudo apt install ffmpeg
```

- Установите все библиотеки для Python:

```bash
pip install -r requirements.txt
```

- Укажите свои API ключи для использования бота:

```bash
export TELEGRAM_BOT_API_KEY=<telegram_bot_api_key>
export OPENAI_API_KEY=<openai_api_key>
```

- Укажите разрешенные ID пользователей:
```bash
export ALLOWED_USERS_ID=<user_id_1>,<user_id_2>,<user_id_3>
```

> В случае необходимости, замените модель нейронной сети на нужную в файле `misc/technical_information.py`.

## Использование

- Запустите файл `run.py`:

```bash
python3.11 run.py
```

## Telegram Bot API

Для создания этого бота была задействована библиотека pyTelegramBotAPI. Больше информации вы найдете здесь:Для создания
этого бота была задействована библиотека pyTelegramBotAPI. Больше информации вы найдете
здесь:[клик](https://github.com/eternnoir/pyTelegramBotAPI)