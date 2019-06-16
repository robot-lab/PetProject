from pymongo import MongoClient

'''connect to db'''
client = MongoClient("mongodb+srv://virrius:QWErty@cluster0-2yjj1.mongodb.net/test?retryWrites=true&w=majority")
print(client.db.list_collection_names())
print(client.database_names())
db = client.get_database("test")
print(db.list_collection_names())


''' create collection and insert one'''
events = db.events
event = {"title": "title1",
         "id": "id1",
         "city": "city1",
         "address": "addr1",
         "date": "date1",
         "category": "cat1",
         "description": "desc1",
         "tags": ["tag1"],
         "weight": 0.5}
events.insert_one(event)

print(events)