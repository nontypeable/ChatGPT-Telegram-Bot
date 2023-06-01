import main

if __name__ == '__main__':
	try:
		main.app.run()
	except Exception as e:
		main.logger.exception(e)
		print(e)