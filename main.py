import telebot

import random
from telebot import types

import os 
import shikimori
import database
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s - %(message)s")


# env[ironment]
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)

answers = {
  "hello": "hi",
  "how are you doing?" : "well",
  "9^2": "81",  
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  for key in answers:
    bttn = types.KeyboardButton(key)
    markup.add(bttn)
  bot.reply_to(message, "Howdy, how are you doing?", reply_markup=markup)


# /anime
@bot.message_handler(commands=['anime'])
def recomendations(message): 
  genres = database.get_genres(message.from_user.id)
  res = shikimori.search(genres)
  
  # anime = random.choice(res['results'])
  anime = res
  
  message_text = f"Title: {anime['russian']}\nStatus: {anime['status']}"

  bot.reply_to(message, message_text)
  
  logging.info("recomendations %s %s", anime['name'], message.from_user.id)

  image_url = 'https://shikimori.one' + anime['image']['original']

  anime_url = 'https://shikimori.one' + anime['url']

  markup = types.InlineKeyboardMarkup(row_width=2)
  bttn = types.InlineKeyboardButton('follow the shikimori link',url=anime_url )
  markup.add(bttn)

  bot.send_photo(message.from_user.id, image_url,reply_markup=markup)

GENRE_ADDED = '✅'
GENRE_NOT_ADDED = '❌'

@bot.message_handler(commands=['genre'])
def genre(message):
  markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)

  user_genres = database.get_genres(message.from_user.id) # []
  
  buttons = []

  for key in sorted(shikimori.genres):
    text = key
    if shikimori.genres[key] in user_genres:
      text = GENRE_ADDED + text
    else: 
      text = GENRE_NOT_ADDED + text

    bttn = types.KeyboardButton(text)
    buttons.append(bttn)
    
  logging.info("genre %s",message.from_user.id)
  # buttons = [btn, btn, ...]
  # markup.add(btn, btn, btn)
  markup.add(*buttons)

  bot.reply_to(message, "Choose genre:", reply_markup=markup)

# user_genres = {}

@bot.message_handler(func=lambda m: m.text[1:] in shikimori.genres)
def genre_pick(message):
  user_genres = database.get_genres(message.from_user.id) # [ 1, 23, 4 ]

  genre_name = message.text[1:]
  genre_id = shikimori.genres[genre_name] # 1
  
  if genre_id in user_genres:
    user_genres.remove(genre_id)
  else:
    user_genres.append(genre_id)
  
  database.update_genres(message.from_user.id, user_genres)
  
  print(user_genres)
  genre(message)
  

@bot.message_handler(func=lambda m: True)
def echo_all(message):
  answer = answers.get(message.text)
  
  if answer is None:
    answer = "hohohoo"
  bot.reply_to(message,answer)
  print (answer) 

logging.info('Starting bot')

bot.polling()


# for fruit in fruits:
#   print(fruit)

# # for (int i = 5; i < 15; i++)
# for i in range(10):
#   print(i)

# for r in range(5,15):
#   print (r)

# dict = {
#   "name": "  ",
#   "age": 15,
#   "phone": "1234567"
# }

# for f,v in dict.items():
#   print (f,v)