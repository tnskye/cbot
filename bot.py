# -*- coding: utf-8 -*-

import config
import telebot
from curling import Curlinger
from whitelist import WhiteLister

bot = telebot.TeleBot(config.ttoken)
whitelist = WhiteLister()

#cur = Curlinger(config.ctoken)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = 'Отстань противный'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['register'])
def handle_register(message):
    text = str(message.chat.id) + ' OK' + message.text[9:]
    #text = 'OK'
    bot.send_message(message.chat.id, text)
    whitelist.update_whitelist(str(message.chat.id), message.text[9:])


@bot.message_handler(commands=['where'])
def handle_where(message):
    token = whitelist.get_account_token(str(message.chat.id))
    if token == None:
        text = 'А ты недоверенный!'
    else:
        item_type = message.text[7:]
        cur = Curlinger(token)

        if not cur.check_item_type(item_type):
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(*[telebot.types.InlineKeyboardButton(text = name, callback_data = name) for name in cur.get_known_types()])
            msg = bot.send_message(message.chat.id, 'Выбирай:', reply_markup=keyboard)

        else:
            text = cur.get_type(item_type)
            bot.send_message(message.chat.id, text)

@bot.callback_query_handler(func=lambda c: True)
def handle_items(c):
    token = whitelist.get_account_token(str(c.message.chat.id))
    cur = Curlinger(token)

    text = cur.get_type(c.data)
    bot.send_message(c.message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['mykeys'])
def handle_mykeys(message):
    token = whitelist.get_account_token(str(message.chat.id))
    if token == None:
        text = 'А ты недоверенный!'
    else:
        keyname = message.text[8:]
        if not keyname:
                
            whitelist.update_states(str(message.chat.id), 'mykeys')

            text = 'Сложно без названия портала найти. Давай пиши название.'
        else:
            cur = Curlinger(token)
            text = cur.search_my_keys(keyname)

    bot.send_message(message.chat.id, text, parse_mode='html')

@bot.message_handler(commands=['city'])
def handle_mykeys(message):
    token = whitelist.get_account_token(str(message.chat.id))
    if token == None:
        text = 'А ты недоверенный!'
    else:
        keyname = message.text[8:]
        if not keyname:
            whitelist.update_states(str(message.chat.id), 'citykeys')
            text = 'Сложно без названия портала найти. Давай пиши название.'
        else:
            cur = Curlinger(token)
            text = cur.search_city_keys(keyname)

    bot.send_message(message.chat.id, text, parse_mode='html')

@bot.message_handler(commands=['empty'])
def handle_empty(message):
    token = whitelist.get_account_token(str(message.chat.id))
    if token == None:
        text = 'А ты недоверенный!'
    else:
        cur = Curlinger(token)
        text = cur.get_empty_space()
    bot.send_message(message.chat.id, text, parse_mode='html')
    
    
# Обработчик text'а
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    token = whitelist.get_account_token(str(message.chat.id))
    if token == None:
        text = 'А ты недоверенный!'

    else:
        cur = Curlinger(token)
        state = whitelist.get_states(str(message.chat.id))

        if state == None:
            text = "Что-то ты мне не нравишься."

        if state == 'mykeys':
            whitelist.clear_states(str(message.chat.id))

            keyname = message.text
            text = cur.search_my_keys(keyname)

        if state == 'citykeys':
            whitelist.clear_states(str(message.chat.id))

            keyname = message.text
            text = cur.search_city_keys(keyname)

    bot.send_message(message.chat.id, text, parse_mode='html')

if __name__ == '__main__':
    bot.polling(none_stop=True)
