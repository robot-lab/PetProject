from pymongo import MongoClient
import csv



'''connect to db'''
client = MongoClient("mongodb://127.0.0.1:27017/")
print(client.db.list_collection_names())
print(client.database_names())
db = client.get_database("events")
print(db.list_collection_names())


''' create collection and insert one'''
events = db.events

with open("data.csv") as csvfile:
    reader = csv.DictReader(csvfile, quotechar='"')
    for row in reader:
        events.insert_one({y: row[y] for y in row.keys() if y})
