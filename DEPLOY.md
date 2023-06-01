## Деплой бота на сервер

> Все дальнейшие действия предназначены для Debian 11

- Обновите систему:

```bash
sudo apt update && sudo apt upgrade
```

- Установите Python:

```bash
sudo apt install python3.9-full
```

- Склонируйте бота в директорию `~/code/chatgpt-telegram-bot`

```shell
mkdir ~/code/
git clone https://gitlab.com/nontypeable/chatgpt-telegram-bot.git ~/code/chatgpt-telegram-bot
cd ~/code/chatgpt-telegram-bot
```

- Добавьте свои переменные окружения:

> `ALLOWED_USERS_ID` в формате _123456789_

```bash
nvim ~/code/chatgpt-telegram-bot/chatgpt-bot/env.env
```

`TELEGRAM_BOT_API_KEY` - токен бота.
`OPENAI_API_KEY` - токен для доступа к OpenAI API.
`ALLOWED_USERS_ID` - это строка, содержащая ID допущенных к использованию пользователей.

- Установите все нужные библиотеки:

```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Настроим systemd-юнит для автоматического запуска бота:

`/etc/systemd/system/chatgpt-bot.service:`
```bash
[Unit]  
Description=ChatGPT Telegram bot
After=network.target

[Service]  
User=<username>
WorkingDirectory=/home/$USER/code/chatgpt-telegram-bot/chatgpt-bot
Restart=always
RestartSec=10s
ExecStart=/path/to/python /home/andrey/code/chatgpt-telegram-bot/chatgpt-bot/run.py
ExecStop=/usr/bin/pkill -f run.py

[Install]
WantedBy=multi-user.target
```