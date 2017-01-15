import config
import telebot
from telebot import types

constant_choose_wine = 'Выбрать вино'
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

@bot.message_handler(commands=['start', 'help'])
def default_message(message): 
	keyboard = types.ReplyKeyboardMarkup()
	button = types.KeyboardButton(constant_choose_wine)
	keyboard.add(button)
	bot.send_message(message.chat.id, "Мы подберем самое подходящее вино специально для вас!", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == constant_choose_wine or message.text == command_choose_wine)
def start_poll(message):
	create_keyboard_with_buttons(message.chat.id, "Выберите цвет: ", variants_of_type)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
	if call.message:
		if call.data in variants_of_type:
			keyboard = types.InlineKeyboardMarkup()
			for i in variants_of_country:
				button = types.InlineKeyboardButton(text=i, callback_data=i)
				keyboard.add(button)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text+" "+call.data, reply_markup=keyboard)
			
		elif call.data in variants_of_country:
			keyboard = types.InlineKeyboardMarkup()
			for i in variants_of_taste:
				button = types.InlineKeyboardButton(text=i, callback_data=i)
				keyboard.add(button)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text+" "+call.data, reply_markup=keyboard)
			
		elif call.data in variants_of_taste:
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text+" "+call.data+"\nВам подойдет: ...")
			

def create_keyboard_with_buttons(chat_id, title, buttons):
	keyboard = types.InlineKeyboardMarkup()
	for i in buttons:
		button = types.InlineKeyboardButton(text=i, callback_data=i)
		keyboard.add(button)
	bot.send_message(chat_id, title, reply_markup=keyboard)

if __name__ == '__main__':
	bot.polling(none_stop=True)