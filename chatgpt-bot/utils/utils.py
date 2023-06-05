import os
import time

import openai
import telebot

import main


# Функция-декоратор для аутентификации пользователей.
def auth(func):
	def wrapper(message: telebot.types.Message):
		if message.from_user.id not in list(
				map(int, os.getenv("ALLOWED_USERS_ID").split(','))):  # список id пользователей, которым разрешен доступ
			main.bot.reply_to(message, "⛔ Вы не допущены к использованию этого бота.")
		else:
			return func(message)

	return wrapper


# Функция для отправки запроса openai.
def openai_request(openai_model: str = "gpt-3.5-turbo", max_tokens: int = 2048, temperature: int = 0, top_p: float = 0.1, *, content: str, context: str, message: telebot.types.Message):
	try:
		openai.api_key = os.getenv("OPENAI_API_KEY")
		completion = openai.ChatCompletion.create(
			model=openai_model,
			messages=[
				{"role": "user", "content": content},
				{"role": "system", "content": context}
			],
			max_tokens=max_tokens,
			temperature=temperature,
			top_p=top_p
		)
		main.bot.send_message(message.chat.id, completion.choices[0].message.content, parse_mode="Markdown")
	except Exception as e:
		main.logger.exception(e)
		waiting_time = 20

		msg = main.bot.send_message(message.chat.id, f"⚠️ Попробуйте отправить запрос ещё раз через {waiting_time} сек.")

		while waiting_time != 0:
			waiting_time -= 1
			main.bot.edit_message_text(chat_id=message.chat.id, text=f"⚠️ Попробуйте отправить запрос ещё раз через {waiting_time} сек.", message_id=msg.message_id)
			time.sleep(1)

		if waiting_time == 0:
			main.bot.delete_message(message.chat.id, msg.message_id)
			main.bot.send_message(message.chat.id, "⚡ Отправьте запрос заново!")


# Функция для создания необходимых для работы бота директорий.
def initialization():
	path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	try:
		if not os.path.exists(f"{path}/audios"):
			os.mkdir(f"{path}/audios")
		if not os.path.exists(f"{path}/images"):
			os.mkdir(f"{path}/images")
		if not os.path.exists(f"{path}/logs"):
			os.mkdir(f"{path}/logs")
	except Exception as e:
		main.logger.exception(e)
