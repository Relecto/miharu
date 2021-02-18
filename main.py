import telebot
import requests
import json
import random
from telebot import types

import os 

# env[ironment]
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)

answers = {
  "hello": "hi",
  "how are you doing?" : "well",
  "9^2": "81",
  
}


genres = {
  'Action': 1,
  'Adventure': 2,
  'Cars': 3,
  'Comedy': 4,
  'Dementia': 5,
  'Demons': 6,
  'Mystery': 7,
  'Drama': 8,
  'Ecchi': 9,
  'Fantasy': 10,
  'Game': 11,
  'Hentai': 12,
  'Historical': 13,
  'Horror': 14,
  'Kids': 15,
  'Magic': 16,
  'Martial Arts': 17,
  'Mecha': 18,
  'Music': 19,
  'Parody': 20,
  'Samurai': 21,
  'Romance': 22,
  'School': 23,
  'Sci Fi': 24,
  'Shoujo': 25,
  'Shoujo Ai': 26,
  'Shounen': 27,
  'Shounen Ai': 28,
  'Space': 29,
  'Sports': 30,
  'Super Power': 31,
  'Vampire': 32,
  'Yaoi': 33,
  'Yuri': 34,
  'Harem': 35,
  'Slice Of Life': 36,
  'Supernatural': 37,
  'Military': 38,
  'Police': 39,
  'Psychological': 40,
  'Thriller': 41,
  'Seinen': 42,
  'Josei': 43
}

# https://api.jikan.moe/v3/search/anime?genre=4&page=1


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  # itembtn1 = types.KeyboardButton('a')
  # itembtn2 = types.KeyboardButton('v')
  # itembtn3 = types.KeyboardButton('d')
  # itembtn4 = types.KeyboardButton('b')
  # itembtn5 = types.KeyboardButton('h')
  # markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
  for key in answers:
    bttn = types.KeyboardButton(key)
    markup.add(bttn)
  bot.reply_to(message, "Howdy, how are you doing?", reply_markup=markup)

page_number = 1
def jikan_search(genres):
  global page_number
  
  answer = requests.get('https://api.jikan.moe/v3/search/anime', params={
    'genre': genres,
    # 'genre_exclude':1,
    'order_by': 'start_date',
    'page':page_number,
  })

  if answer.status_code == 404:
    page_number = 1

    answer = requests.get('https://api.jikan.moe/v3/search/anime', params={
      'genre': genres,
      # 'genre_exclude':1,
      'order_by': 'start_date',
      'page':page_number,
    })

  page_number +=1

  return json.loads(answer.text)


# /anime
@bot.message_handler(commands=['anime'])
def recomendations(message): 
  genres = user_genres.get(message.from_user.id, [])
  res = jikan_search(genres)
  
  anime = random.choice(res['results'])
  
  bot.reply_to(message, anime['title'])
  print(anime['title'])
  bot.send_photo(message.from_user.id,anime['image_url'])


@bot.message_handler(commands=['genre'])
def genre(message):
  markup = types.ReplyKeyboardMarkup(row_width=2)
  for key in genres:
    bttn = types.KeyboardButton(key)
    markup.add(bttn)
  bot.reply_to(message, "Choose genre:", reply_markup=markup)

user_genres = {}

@bot.message_handler(func=lambda m: m.text in genres)
def genre_pick(message):
  bot.reply_to(message, message.text)

  if message.from_user.id not in user_genres:
    user_genres[message.from_user.id] = []

  genre_id = genres[message.text]
  if genre_id in user_genres[message.from_user.id]:
    user_genres[message.from_user.id].remove(genre_id)
  else:
    user_genres[message.from_user.id].append(genre_id)
  
  print(user_genres)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
  answer = answers.get(message.text)
  if answer is None:
    answer = "hohohoo"
  bot.reply_to(message,answer)
  print (answer)



  
  
  

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