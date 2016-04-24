##TEST DATA
##name = 'RTSI'
##open_value = 133
##last_change_prc = 5.0
##market_price = 120
from telebot import telebot

with open("news.txt", "r", encoding = "utf-8") as infile:
	text = infile.read()
done = text.split("\n")

names = {
	'MICEXINDEXCF':'ММВБ',
	'RTSI':'РТС'
}

def newsmaker_stocks(name, open_value, market_price, last_change_prc):
	"""
	The function that generates news
	"""
	good_name = names[name]
	if open_value > market_price:
		temp = "Сегодня индекс {} с момента открытия торгов упал на {}% до {} пунктов"
		filled_temp = temp.format(good_name, str(last_change_prc), str(market_price))
	else:
		temp = "Сегодня индекс {} с момента открытия торгов вырос на {}% до {} пунктов"
		filled_temp = temp.format(good_name, str(last_change_prc), str(market_price))
	if filled_temp in done:
		print("dublicate!")
	else:
#		with open("news.txt", 'a', encoding = 'utf-8') as infile:
#			infile.write(filled_temp + '\n')
		telebot(filled_temp)

if __name__ == '__main__':
	newsmaker_stocks(name, open_value, market_price, last_change_prc)