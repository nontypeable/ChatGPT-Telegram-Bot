import logging, os, random, datetime
import uuid

import telebot
import misc
from utils import chatgpt_request, get_text_from_voice, get_text_from_image, initialization, auth, voice_message_downloader, image_downloader
import openai

initialization()
logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG,
	filename=f"logs/{datetime.datetime.now().date()}_{datetime.datetime.now().time()}"
)
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
	bot.send_message(chat_id=message.chat.id,
					 text=chatgpt_request(content=message.text, context=misc.last_message))
	bot.delete_message(message.chat.id, msg.message_id)
	misc.last_message = message.text
	print(misc.last_message)


# Отправка запроса ChatGPT при получении текста с фото.
@bot.message_handler(content_types=["photo"])
@auth
def send_request_via_image(message):
	path = f"{os.path.dirname(os.path.realpath(__file__))}/images/{str(uuid.uuid4())}"
	text = get_text_from_image(path, message)

	reply_msg = bot.send_message(chat_id=message.chat.id, text=f"*Я распознал на изображении:*\n\n{text}", parse_mode="Markdown")

	msg = bot.send_message(chat_id=message.chat.id, text="👨‍💻 Запрос отправлен!")
	bot.reply_to(message=reply_msg, text=chatgpt_request(content=text, context=misc.last_message))
	bot.delete_message(message.chat.id, msg.message_id)


# Отправка запроса ChatGPT при получении текста из голосового сообщения.
@bot.message_handler(content_types=["voice"])
@auth
def send_request_via_voice(message):
	image_path = f"{os.path.dirname(os.path.realpath(__file__))}/audios/{str(uuid.uuid4())}"
	voice_message_text = get_text_from_voice(image_path, message)

	reply_msg = bot.send_message(chat_id=message.chat.id, text=f"*Я распознал в голосовом сообщении:*\n\n{voice_message_text}", parse_mode="Markdown")
	bot.reply_to(message=reply_msg, text=chatgpt_request(content=voice_message_text, context=misc.last_message))