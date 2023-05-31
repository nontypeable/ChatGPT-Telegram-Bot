import os
import uuid

import cv2
import openai
import pytesseract
import speech_recognition as sr
import telebot.types
from pydub import AudioSegment

import main
import misc


# Декоратор для аутентификации пользователей.
def auth(func):
	def wrapper(message: telebot.types.Message):
		if message.from_user.id not in list(
				map(int, os.getenv("ALLOWED_USERS_ID").split(','))):  # список id пользователей, которым разрешен доступ
			main.bot.reply_to(message, "⛔ Вы не допущены к использованию этого бота.")
		else:
			return func(message)

	return wrapper


# Функция для инициализации необходимых для работы бота директорий.
def initialization():
	path = os.path.dirname(os.path.realpath(__file__))
	try:
		if not os.path.exists(f"{path}/audios"):
			os.mkdir(f"{path}/audios")
		if not os.path.exists(f"{path}/images"):
			os.mkdir(f"{path}/images")
		if not os.path.exists(f"{path}/logs"):
			os.mkdir(f"{path}/logs")
	except Exception as e:
		print(e)


def image_downloader(path: str, message: telebot.types.Message):
	try:
		file = main.bot.get_file(message.photo[-1].file_id)
		download_file = main.bot.download_file(file.file_path)
		with open(path, "wb") as image_file:
			image_file.write(download_file)
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."


# Функция для получения текста с изображения. (beta)
def get_text_from_image(image_path: str, message: telebot.types.Message):  # В абсолютном пути к файлу не указывать его расширение!
	try:
		image_downloader(image_path, message)
		img = cv2.imread(image_path)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
		# ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
		text = pytesseract.image_to_string(img, lang="rus+eng").replace("-", "")  # .replace("\n", " ")
		os.remove(image_path)
		return text
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."

def voice_message_downloader(path: str, message: telebot.types.Message):  # В абсолютном пути к файлу не указывать его расширение!
	try:
		file = main.bot.get_file(message.voice.file_id)
		download_file = main.bot.download_file(file.file_path)
		with open(f"{path}.ogg", "wb") as audio_file:
			audio_file.write(download_file)
		audio = AudioSegment.from_ogg(f"{path}.ogg")
		audio.export(f"{path}.wav", format="wav")
		os.remove(f"{path}.ogg")
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."

# Функция для получения текста из голосового сообщения.
def get_text_from_voice(path: str, messsage: telebot.types.Message):  # Передавать исключительно переменную с путем. Без расширения.
	try:
		voice_message_downloader(path, messsage)
		recognizer = sr.Recognizer()
		with sr.AudioFile(f"{path}.wav") as source:
			audio = recognizer.record(source)
		text = recognizer.recognize_google(audio, language="ru-RU")
		os.remove(f"{path}.wav")
		return text
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."


# Функция для отправки запроса ChatGPT.
def chatgpt_request(*, openai_model: str = "gpt-3.5-turbo", openai_max_tokens: int = 2048, openai_temperature: int = 0,
					openai_top_p: float = 0.1,
					content: str,
					context: str):
	openai.api_key = os.getenv("OPENAI_API_KEY")
	try:
		chat_completion = openai.ChatCompletion.create(
			model=openai_model,
			messages=[
				{"role": "system", "content": context},
				{"role": "user", "content": content}
			],
			max_tokens=openai_max_tokens,
			temperature=openai_temperature,
			top_p=openai_top_p
		)
		return chat_completion.choices[
			0].message.content  # При смене модели может понадобиться корректирование этой строки.
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."
