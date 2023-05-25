import datetime
import logging
import os
import random

import telebot

from misc import technical_information, welcome_text
from utils import chatgpt_request, get_text_from_voice, get_text_from_image, initialization

initialization()
logging.basicConfig(level=logging.DEBUG,
					filename=f"logs/{datetime.datetime.now().date()}_{datetime.datetime.now().time()}")
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_API_KEY"))


# Приветствие.
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
	if message.chat.id in technical_information.allowed_users:
		bot.send_message(chat_id=message.chat.id, text=welcome_text.welcome_text)
	else:
		bot.send_message(chat_id=message.chat.id, text="Вы не допущены к использованию.")


# Отправка запроса ChatGPT при получении сообщения в виде текста.
@bot.message_handler(content_types=["text"])
def neural_network_request(message):
	if message.chat.id in technical_information.allowed_users:
		msg = bot.send_message(chat_id=message.chat.id, text="👨‍💻 Запрос отправлен!")
		bot.send_message(chat_id=message.chat.id, text=chatgpt_request(content=message.text, context=technical_information.old_message))
		bot.delete_message(message.chat.id, msg.message_id)
		technical_information.old_message = message.text
	else:
		bot.send_message(chat_id=message.chat.id, text="Вы не допущены к использованию.")


# Отправка запроса ChatGPT при получении текста с фото.
@bot.message_handler(content_types=["photo"])
def send_text_from_image(message):
	if message.chat.id in technical_information.allowed_users:
		# Загрузка изображения.
		file = bot.get_file(message.photo[-1].file_id)
		downloaded_file = bot.download_file(file.file_path)
		path = f"./images/{str(random.randint(1, 10000))}"
		with open(path, "wb") as new_file:
			new_file.write(downloaded_file)

		msg = bot.send_message(chat_id=message.chat.id, text="👨‍💻 Запрос отправлен!")
		text = get_text_from_image(path)
		reply_msg = bot.send_message(chat_id=message.chat.id, text=text)
		bot.reply_to(message=reply_msg, text=chatgpt_request(content=text,context=technical_information.old_message))
		bot.delete_message(message.chat.id, msg.message_id)
	else:
		bot.send_message(chat_id=message.chat.id, text="Вы не допущены к использованию.")


# Отправка запроса ChatGPT при получении текста из голосового сообщения.
@bot.message_handler(content_types=["voice"])
def send_text_from_voice(message):
	if message.chat.id in technical_information.allowed_users:
		# Загрузка аудио файла.
		file = bot.get_file(message.voice.file_id)
		downloaded_file = bot.download_file(file.file_path)
		path = f"./audios/{str(random.randint(10001, 20000))}"
		with open(f"{path}.ogg", "wb") as new_file:
			new_file.write(downloaded_file)

		msg = bot.send_message(chat_id=message.chat.id, text="👨‍💻 Запрос отправлен!")
		text = get_text_from_voice(path)
		reply_msg = bot.send_message(chat_id=message.chat.id, text=f"Я распознал вашем голосовом сообщении:\n\n{text}")
		bot.reply_to(message=reply_msg, text=chatgpt_request(content=text,context=technical_information.old_message))
		bot.delete_message(message.chat.id, msg.message_id)
	else:
		bot.send_message(chat_id=message.chat.id, text="Вы не допущены к использованию.")
