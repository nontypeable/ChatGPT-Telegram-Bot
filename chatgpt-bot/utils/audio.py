import os

import speech_recognition as sr
import telebot
from pydub import AudioSegment

import main


class Audio:
	def __init__(self, path, message):
		self.path = path
		self.message = message
		self.__voice_message_downloader(self.path, self.message)

	# Метод для загрузки и конвертации голосового сообщения в wav.
	def __voice_message_downloader(self, path: str, message: telebot.types.Message):  # В абсолютном пути к файлу не указывать его расширение!
		try:
			file = main.bot.get_file(message.voice.file_id)
			download_file = main.bot.download_file(file.file_path)
			with open(f"{path}.ogg", "wb") as audio_file:
				audio_file.write(download_file)
			audio = AudioSegment.from_ogg(f"{path}.ogg")
			audio.export(f"{path}.wav", format="wav")
			os.remove(f"{path}.ogg")
		except Exception as e:
			main.logger.exception(e)
			return "Произошла ошибка, попробуйте ещё раз чуть позже."

	# Метод для получения текста из аудио файла.
	def voice_message_recognition(self, path: str):  # Передавать исключительно переменную с путем. Без расширения.
		try:
			recognizer = sr.Recognizer()
			with sr.AudioFile(f"{path}.wav") as source:
				audio = recognizer.record(source)
			text = recognizer.recognize_google(audio, language="ru-RU")
			os.remove(f"{path}.wav")
			return text
		except Exception as e:
			main.logger.exception(e)
			return "Произошла ошибка, попробуйте ещё раз чуть позже."
