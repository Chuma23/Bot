import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import re

datas = {
	'os_username':'m.chumakov',
	'os_password':'sZcu3#4'
}

bot = telebot.TeleBot('1317807668:AAHcNPFcffisqpq0evZtgX-M0in5bIc0uzs')

@bot.message_handler(commands=['start'])
def start_message(message):
	keyboard = types.InlineKeyboardMarkup() 
	key_info = types.InlineKeyboardButton(text='Контакты', callback_data='info') 
	keyboard.add(key_info) 

	key_sup = types.InlineKeyboardButton(text='Узнать состояние заявки', callback_data='sup') 	
	keyboard.add(key_sup) 

	key_stiker = types.InlineKeyboardButton(text='Стикерпак', callback_data='stiker') 
	keyboard.add(key_stiker)

	bot.send_message(message.from_user.id, text='Вырите действие:', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)


# Обработчик нажатий на кнопки 
@bot.callback_query_handler(func=lambda call: True) 
def callback_worker(call):
	if call.data == "info":
		try:
			response = requests.get('http://www.rostu-comp.ru/')
			soup = BeautifulSoup(response.text, 'lxml')
			if response.status_code == 200:
				print('Success!')
				##msg = soup.em.text
				msg= soup.find("div", { "class" : "item phone"}).span.text
				msg1 = soup.find("div", { "class" : "item mail"}).text
				#re.sub("^\s+|\n|\r|\s+$", '', msg1) # не работает
				msg2 = soup.find("div", { "class" : "item adress"}).p.text
				bot.send_message(call.message.chat.id, 'Телефон: '+msg.strip()+ 
				'\nЭлектронная почта: '+msg1.strip()+
				'\nАдрес: '+msg2.strip())
			elif response.status_code == 404:
				bot.send_message(call.message.chat.id, 'Ошбика 404')
				print('Ошибка 404')

		except requests.ConnectionError:
			bot.send_message(call.message.chat.id, 'Извите ошибка соединения с сайтом')
			print('Извите ошибка соединения с сайтом')
	

	if call.data == "sup": 
		bot.send_message(call.message.chat.id, "Введите номер заявки")
		

	if call.data == "stiker": 
		bot.send_message(call.message.chat.id, "Ссылка на стикер пак")
	bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Здравствуйте, это компания РОСТУ, введите "Привет" для начала работы.')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text.lower() == "привет": 
		keyboard = telebot.types.ReplyKeyboardMarkup(True)
		keyboard.row('/start', '/help')
		bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

	else:
		bot.send_message(message.from_user.id, 'Я вас не понимаю. Напиши "Привет" или выберите команду.')

bot.polling(none_stop=True, interval=0)


#1317807668:AAHcNPFcffisqpq0evZtgX-M0in5bIc0uzs
