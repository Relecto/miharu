import requests
import json

from dataclasses import dataclass, field

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:86.0) Gecko/20100101 Firefox/86.0'
}


@dataclass
class Anime:
  name: str
  russian: str
  id: int
  image: dict
  url: str
  kind: str
  score: float
  status: str
  episodes: int
  episodes_aired: int
  aired_on: int
  released_on: int
  rating: str = ""
  english: list = field(default_factory=list)
  japanese: list = field(default_factory=list)
  synonyms: list = field(default_factory=list)
  license_name_ru: str = ""
  duration: int = 0
  description: str = ""
  description_html: str = ""
  description_source: str = ""
  franchise: str = ""
  favoured: bool = False
  anons: bool = False
  ongoing: bool = False
  thread_id: int = 0
  topic_id: int = 0
  myanimelist_id: int = 0
  rates_scores_stats: list = field(default_factory=list)
  rates_statuses_stats: list = field(default_factory=list)
  updated_at: str = ""
  next_episode_at: str = ""
  fansubbers: list = field(default_factory=list)
  fandubbers: list = field(default_factory=list)
  licensors: list = field(default_factory=list)
  genres: list = field(default_factory=list)
  studios: list = field(default_factory=list)
  videos: list = field(default_factory=list)
  screenshots: list = field(default_factory=list)
  user_rate: int = 0




def search(genres):
  answer = requests.get('https://shikimori.one/api/animes', headers=headers, params={
    'genre': genres,
    'genre_exclude':1,
    'order': 'random',
  })
  res = json.loads(answer.text) 
  
  return Anime(**res [0]) 

def genre():
  answer = requests.get('https://shikimori.one/api/genres', headers=headers)
  r = json.loads(answer.text)
  genres = [ genre for genre in r if genre['kind'] == 'anime' ]
  dictionary = {}

  for genre in genres: 
    name = genre['russian']
    genre_id = genre['id']

    dictionary[name] = genre_id
    
  return dictionary


def get_anime(id): 
  answer = requests.get('https://shikimori.one/api/animes/'+str(id), headers=headers)
  if answer.status_code == 404:
    raise Exception("Error. Anime was not found.")
  res = json.loads(answer.text)
  return Anime(**res)

genres_ru = {
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

genres_en = {
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

# shikimori.genres[message.settings['language']]
genres = {
  'ru': genres_ru,
  'en': genres_en,
}