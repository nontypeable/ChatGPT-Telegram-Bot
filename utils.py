import os

import cv2
import openai
import pytesseract
import speech_recognition as sr
from pydub import AudioSegment

from misc import technical_information


# Метод для инициализации необходимых для работы бота директорий.
def initialization():
	try:
		if not os.path.exists("audios"):
			os.mkdir("audios")
		if not os.path.exists("images"):
			os.mkdir("images")
		if not os.path.exists("logs"):
			os.mkdir("logs")
	except Exception as e:
		print(e)


# Метод для получения текста с изображения. (beta)
def get_text_from_image(path: str):  # В абсолютном пути к файлу не указывать его расширение!
	try:
		img = cv2.imread(path)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
		text = pytesseract.image_to_string(img, lang="rus+eng").replace("-", "")  # .replace("\n", " ")
		os.remove(path)
		return text
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."


# Метод для конвертирования голосового сообщения в формат wav. (beta)
def ogg_to_wav(path: str):  # В абсолютном пути к файлу не указывать его расширение!
	try:
		audio = AudioSegment.from_ogg(f"{path}.ogg")
		audio.export(f"{path}.wav", format="wav")
		os.remove(f"{path}.ogg")
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."


# Метод для получения текста из голосового сообщения.
def get_text_from_voice(path: str):  # Передавать исключительно переменную с путем. Без расширения.
	try:
		ogg_to_wav(path)
		recognizer = sr.Recognizer()
		with sr.AudioFile(f"{path}.wav") as source:
			audio = recognizer.record(source)
		text = recognizer.recognize_google(audio, language="ru-RU")
		os.remove(f"{path}.wav")
		return text
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."


# Метод для отправки запроса ChatGPT.
def chatgpt_request(content: str):
	openai.api_key = os.getenv("OPENAI_API_KEY")
	try:
		chat_completion = openai.ChatCompletion.create(
			model=technical_information.openai_gpt_model_name,
			messages=[
				{"role": "user", "content": content}
			],
			max_tokens=technical_information.openai_gpt_max_tokens,
			temperature=technical_information.openai_gpt_temperature,
			top_p=technical_information.openai_gpt_top_p
		)
		return chat_completion.choices[
			0].message.content  # При смене модели может понадобиться корректирование этой строки.
	except:
		return "Произошла ошибка, попробуйте ещё раз чуть позже."
