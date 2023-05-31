import main
from utils.utils import initialization

if __name__ == '__main__':
	try:
		initialization()
		main.bot.infinity_polling()
	except Exception as e:
		main.logger.exception(e)
		print(e)