from pymongo import MongoClient
import json
from bson import json_util


'''connect to db'''
uri = "mongodb://mongo-admin:5NtrzVq9TKOVVtnSBMLcdVVMLyTjHhihb2Ft0mWBsA2ZZErxjAKX10UOIdfBbFif3m6anbqx4mkzUZslSA9mvQ==@mongo-admin.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = MongoClient(uri)
#client = MongoClient("mongodb+srv://virrius:QWErty@cluster0-2yjj1.mongodb.net/test?retryWrites=true&w=majority")
print(client.db)
#print(client.list_database_names())
db = client.get_database("test")



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
#events.insert_one(event)
print(events)
el=[el for el in db.test.find()]
print(el)
print(json.dumps(el, sort_keys=True, indent=4, default=json_util.default))
