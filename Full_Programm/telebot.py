import re
from twx.botapi import TelegramBot, ReplyKeyboardMarkup

users = []

def telebot(news):
	"""
	This Telegram bot sends a message about stock news to a user using 
	TWX bot library. More about this library may be find at:
	https://pythonhosted.org/twx/twx/botapi/botapi.html#module-twx.botapi
	"""
	bot = TelegramBot('182387487:AAGiA489MZtosNOkhLjzo3_6l7xCYkG4N5A')
	bot.update_bot_info().wait()
	updates = bot.get_updates().wait()
	for update in updates:
	    user_id, = re.findall("sender=User.id=(\d+)", str(update))
	    if user_id not in users:
	    	users.append(user_id)
	for user in users:
		user_id = int(user)
		bot.send_message(user_id, news)

if __name__ == '__main__':
	telebot(news)

