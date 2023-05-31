import os

import cv2
import pytesseract
import telebot

import main


class Image:
	def __init__(self, path: str, message: telebot.types.Message):
		self.path = path
		self.message = message
		self.__image_downloader(self.path, self.message)

	# Метод для загрузки изображений из чата.
	def __image_downloader(self, path: str, message: telebot.types.Message):
		try:
			file = main.bot.get_file(message.photo[-1].file_id)
			download_file = main.bot.download_file(file.file_path)
			with open(path, "wb") as image_file:
				image_file.write(download_file)

		except Exception as e:
			main.logger.exception(e)
			return "Произошла ошибка, попробуйте ещё раз чуть позже."

	# Метод для получения текста с изображений.
	def image_recognition(self, image_path: str):  # В абсолютном пути к файлу не указывать его расширение!
		try:
			img = cv2.imread(image_path)
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			text = pytesseract.image_to_string(img, lang="rus+eng").replace("-", "")  # .replace("\n", " ")
			os.remove(image_path)
			return text

		except Exception as e:
			main.logger.exception(e)
			return "Произошла ошибка, попробуйте ещё раз чуть позже."
