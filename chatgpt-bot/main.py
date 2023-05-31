import datetime
import logging
import os
import uuid

import openai
import telebot

import misc
from utils.audio import Audio
from utils.image import Image
from utils.utils import auth, openai_request, initialization

initialization()
logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG,
	filename=f"chatgpt-bot/logs/{datetime.datetime.now().date()}_{datetime.datetime.now().time()}"
)
logger = logging.getLogger(__name__)
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_API_KEY"))


# Приветствие.
@bot.message_handler(commands=["start", "help"])
@auth
def send_welcome(message):
	bot.send_message(chat_id=message.chat.id, text=misc.welcome_text)


# Метод для очистки контекста чата.
@bot.message_handler(commands=["clearcontext"])
@auth
def clear_context(message):
	chat_completion = openai.ChatCompletion()
	chat_completion.clear()
	bot.send_message(chat_id=message.chat.id, text="Контекст чата очищен.")


# Отправка запроса ChatGPT при получении сообщения в виде текста.
@bot.message_handler(content_types=["text"])
@auth
def send_request_via_text(message):
	msg = bot.send_message(chat_id=message.chat.id, text="👨‍💻 Запрос отправлен!")

	bot.send_message(chat_id=message.chat.id, text=openai_request(content=message.text, context=misc.last_message))
	bot.delete_message(message.chat.id, msg.message_id)
	misc.last_message = message.text


# Отправка запроса ChatGPT при получении текста с фото.
@bot.message_handler(content_types=["photo"])
@auth
def send_request_via_image(message):
	image_path = f"{os.path.dirname(os.path.realpath(__file__))}/images/{str(uuid.uuid4())}"

	image = Image(image_path, message)
	text = image.image_recognition(image_path)

	reply_msg = bot.send_message(chat_id=message.chat.id, text=f"*Я распознал на изображении:*\n\n{text}", parse_mode="Markdown")

	msg = bot.send_message(chat_id=message.chat.id, text="👨‍💻 Запрос отправлен!")
	bot.reply_to(message=reply_msg, text=openai_request(content=text, context=misc.last_message))
	bot.delete_message(message.chat.id, msg.message_id)


# Отправка запроса ChatGPT при получении текста из голосового сообщения.
@bot.message_handler(content_types=["voice"])
@auth
def send_request_via_voice(message):
	audio_path = f"{os.path.dirname(os.path.realpath(__file__))}/audios/{str(uuid.uuid4())}"

	audio = Audio(audio_path, message)
	text = audio.voice_message_recognition(audio_path)

	reply_msg = bot.send_message(chat_id=message.chat.id, text=f"*Я распознал в голосовом сообщении:*\n\n{text}", parse_mode="Markdown")

	msg = bot.send_message(chat_id=message.chat.id, text="👨‍💻 Запрос отправлен!")
	bot.reply_to(message=reply_msg, text=openai_request(content=text, context=misc.last_message))
	bot.delete_message(message.chat.id, msg.message_id)
