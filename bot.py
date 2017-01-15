import config
import telebot
import time
import urllib
from telebot import types

constant_choose_wine = 'Подбор подходящей бутылки вина.'
command_choose_wine = '/wine'

CHW_taste_Bitter = 'Горький'
CHW_taste_Sweet = 'Сладкий'
CHW_taste_Sour = 'Кислый'

CHW_country_Spain = 'Испания'
CHW_country_Italy = 'Италия'
CHW_country_France = 'Франция'

CHW_wine_sparkling = 'Игристое'
CHW_wine_red = 'Красное'
CHW_wine_white = 'Белое'

variants_of_taste = [CHW_taste_Bitter, CHW_taste_Sweet, CHW_taste_Sour]
variants_of_country = [CHW_country_Spain, CHW_country_Italy, CHW_country_France]
variants_of_type = [CHW_wine_sparkling, CHW_wine_red, CHW_wine_white]

bot = telebot.TeleBot(config.token)

url = 'http://www.winebutik.net/assets/images/etiketke/1/50.png'
f = open('out.jpg','wb')
f.write(urllib.request.urlopen(url).read())
f.close()

@bot.message_handler(commands=['start', 'help'])
def default_message(message): 
	keyboard = types.ReplyKeyboardMarkup()
	button = types.KeyboardButton(constant_choose_wine)
	keyboard.add(button)
	bot.send_message(message.chat.id, "Мы подберем самое подходящее вино специально для вас!", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == constant_choose_wine or message.text == command_choose_wine)
def start_poll(message):
	mess = bot.send_message(message.chat.id, "Выбираем ...")
	update_message_with_message_title_buttons(mess,"Выберите цвет:",variants_of_type,"")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
	if call.message:
		if call.data in variants_of_type:
			update_message_with_message_title_buttons(call.message,"Выберите страну:",variants_of_country,call.data)
			
		elif call.data in variants_of_country:
			update_message_with_message_title_buttons(call.message,"Выберите вкус:",variants_of_taste,call.data)
			
		elif call.data in variants_of_taste:
			new_message = update_message_with_message_title_buttons(call.message,"Мы рекомендуем:",[],call.data)
			calculate_best_coincidence_wine(new_message)

def create_keyboard_with_buttons(buttons):
	keyboard = types.InlineKeyboardMarkup()
	for i in buttons:
		button = types.InlineKeyboardButton(text=i, callback_data=i)
		keyboard.add(button)
	return keyboard

def update_message_with_message_title_buttons(message, title, buttons, calldata):
	keyboard = create_keyboard_with_buttons(buttons)
	return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message.text+" "+calldata+"\n"+title, reply_markup=keyboard)

def calculate_best_coincidence_wine(message):
	wine = '«Shadow’s Run» из винограда Шираз и Каберне Совиньон'
	bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message.text+" "+wine)
	send_photo_after_message(message)

def send_photo_after_message(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    img = open('out.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    img.close()

if __name__ == '__main__':
	bot.polling(none_stop=True)