import telebot

import random
from telebot import types

from template import t
import os 
import shikimori
import database
import logging
from helper import escape



logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s - %(message)s")

telebot.apihelper.ENABLE_MIDDLEWARE=True

# env[ironment]
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)

answers = {
  "hello": "hi",
  "how are you doing?" : "well",
  "9^2": "81",  
}



@bot.middleware_handler(update_types=['message'])
def set_settings(bot_instance,message):
  settings = database.get_settings(message.from_user.id) 
  
  if settings == None:
    settings={}
  
  settings.setdefault('language', 'ru')

  message.settings = settings
  


#/start /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  for key in answers:
    bttn = types.KeyboardButton(key)
    markup.add(bttn)
  bot.reply_to(message, "Howdy, how are you doing?", reply_markup=markup)

# /lang en
# /lang ru
# /lang jp
# /lang 
@bot.message_handler(commands=['lang'])
def change_language(message):
  cmd = message.text.split() # ['/lang', 'ru']

  if len(cmd) != 2 or cmd[1] not in ["ru","en"]:
    bot.reply_to(message, t("undefined_lang", message.settings["language"]))
    return
  
  database.update_settings(message.from_user.id, {'language':cmd[1]})
  bot.reply_to(message,t("confirmed_lang",message.settings["language"] ))
  

  
# /anime
@bot.message_handler(commands=['anime'])
def recomendations(message): 
  genres = database.get_genres(message.from_user.id)
  res = shikimori.search(genres) 
  
  anime = shikimori.get_anime(res.id)

  bot.reply_to(message, t("anime_inf",message.settings["language"],anime=anime),parse_mode="MarkdownV2")
  
  logging.info("recomendations %s %s", anime.name, message.from_user.id)

  image_url = 'https://shikimori.one' + anime.image['original']

  anime_url = 'https://shikimori.one' + anime.url

  markup = types.InlineKeyboardMarkup(row_width=2)
  bttn = types.InlineKeyboardButton('follow the shikimori link',url=anime_url )
  markup.add(bttn)

  bot.send_photo(message.from_user.id, image_url,reply_markup=markup)



GENRE_ADDED = '✅'
GENRE_NOT_ADDED = '❌'


#/genre
@bot.message_handler(commands=['genre'])
def genre(message):
  markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)

  user_genres = database.get_genres(message.from_user.id) # []
  
  buttons = []

  for key in sorted(shikimori.genres[message.settings['language']]):
    text = key
    if shikimori.genres[message.settings['language']][key] in user_genres:
      text = GENRE_ADDED + text
    else: 
      text = GENRE_NOT_ADDED + text

    bttn = types.KeyboardButton(text)
    buttons.append(bttn)
    
  logging.info("genre %s",message.from_user.id)

  markup.add(*buttons)

  bot.reply_to(message, "Choose genre:", reply_markup=markup)


# user_genres = {}
@bot.message_handler(func=lambda m: m.text[1:] in shikimori.genres[m.settings['language']])
def genre_pick(message):
  user_genres = database.get_genres(message.from_user.id) 

  genre_name = message.text[1:]
  genre_id = shikimori.genres[message.settings['language']][genre_name] # 1
  
  if genre_id in user_genres:
    user_genres.remove(genre_id)
  else:
    user_genres.append(genre_id)
  
  database.update_genres(message.from_user.id, user_genres)
  
  print(user_genres)
  genre(message)
  

#without command
@bot.message_handler(func=lambda m: True)
def echo_all(message):
  answer = answers.get(message.text)
  
  if answer is None:
    answer = "hohohoo"
  bot.reply_to(message,answer)
  print (answer) 

logging.info('Starting bot')

bot.polling()