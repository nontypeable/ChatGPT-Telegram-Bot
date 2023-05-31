import main

if __name__ == '__main__':
	try:
		main.bot.infinity_polling()
	except Exception as e:
		main.logger.exception(e)
		print(e)