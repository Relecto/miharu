import requests
import json

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:86.0) Gecko/20100101 Firefox/86.0'
}




def search(genres):
  answer = requests.get('https://shikimori.one/api/animes', headers=headers, params={
    'genre': genres,
    'genre_exclude':1,
    'order': 'random',
  })
  res = json.loads(answer.text) # [ {} ]
  
  return res [0] 

def genre():
  answer = requests.get('https://shikimori.one/api/genres', headers=headers)
  r = json.loads(answer.text)
  genres = [ genre for genre in r if genre['kind'] == 'anime' ]
  dictionary = {}

  for genre in genres: # {'id': 17, 'name': 'Martial Arts', 'russian': 'Боевые искусства', 'kind': 'anime'}
    name = genre['russian']
    genre_id = genre['id']

    dictionary[name] = genre_id
    
  # {
  #   "Детектив": 7
  # }

  return dictionary

genres = {
  'Драма': 8, 
  'Игры': 11, 
  'Психологическое': 40, 
  'Приключения': 2, 
  'Музыка': 19, 
  'Экшен': 1, 
  'Комедия': 4, 
  'Демоны': 6, 
  'Полиция': 39,
  'Космос': 29, 
  'Этти': 9, 
  'Фэнтези': 10, 
  'Исторический': 13, 
  'Ужасы': 14, 
  'Магия': 16, 
  'Меха': 18, 
  'Пародия': 20, 
  'Самураи': 21, 
  'Романтика': 22, 
  'Школа': 23, 
  'Сёнен': 27, 
  'Спорт': 30, 
  'Вампиры': 32,  
  'Гарем': 35, 
  'Сёнен-ай': 28, 
  'Повседневность': 36, 
  'Сёдзё-ай': 26, 
  'Дзёсей': 43, 
  'Сверхъестественное': 37, 
  'Триллер': 41, 
  'Фантастика': 24, 
  'Сёдзё': 25, 
  'Супер сила': 31, 
  'Военное': 38, 
  'Детектив': 7, 
  'Детское': 15, 
  'Машины': 3, 
  'Боевые искусства': 17, 
  'Безумие': 5, 
  'Сейнен': 42
}
