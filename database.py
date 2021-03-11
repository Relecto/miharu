import pymongo
import os 

client = pymongo.MongoClient(os.getenv("MONGO_URL"))

"""
{
  'user_id': 123991293,
  'genres': [1,2,3]
}
"""
def get_genres(user_id):
  db = client.bot_miharu
  collection = db.setting_genres
  res = collection.find_one({
    'user_id': user_id,
  }) # None

  if res == None:
    return []
  
  return res['genres']

def update_genres(user_id, genres):
  db = client.bot_miharu
  collection = db.setting_genres
  res = collection.update_one({
    'user_id': user_id,
  }, {
    '$set': { 'genres': genres }
  }, upsert = True )
  return res
  
