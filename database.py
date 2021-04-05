import pymongo
import os 

client = pymongo.MongoClient(os.getenv("MONGO_URL"))

# bot_miharu

"""
{
  'user_id': 123991293,
  'genres': [1,2,3],
  'language': 'en'
}
"""
def get_genres(user_id):
  db = client.bot_miharu
  collection = db.settings
  
  res = collection.find_one({
    'user_id': user_id,
  })
  
  if res == None:
    return []
  
  return res.get('genres', [])

def update_genres(user_id, genres):
  db = client.bot_miharu
  collection = db.settings

  res = collection.update_one({
    'user_id': user_id,
  }, {
    '$set': { 'genres': genres }
  }, upsert = True )
  
  return res

def get_settings(user_id):
  db = client.bot_miharu
  collection = db.settings

  res = collection.find_one({
    'user_id': user_id,
  })
  
  return res


def update_settings(user_id,settings):
  db = client.bot_miharu
  collection = db.settings
  
  res = collection.update_one({
    'user_id': user_id,
  }, {
    '$set': settings
  }, upsert = True ) # upsert = update + insert
  
  return res