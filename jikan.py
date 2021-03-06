import requests
import json


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



page_number = 1
def search(genres):
  global page_number
  
  answer = requests.get('https://api.jikan.moe/v3/search/anime', params={
    'genre': genres,
    'order_by': 'start_date',
    'page':page_number,
  })

  if answer.status_code == 404:
    page_number = 1

    answer = requests.get('https://api.jikan.moe/v3/search/anime', params={
      'genre': genres,
      'order_by': 'start_date',
      'page':page_number,
    })

  page_number +=1

  return json.loads(answer.text)

