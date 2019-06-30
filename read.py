import csv

with open("data.csv") as csvfile:
    reader = csv.DictReader(csvfile, quotechar='"')
    for row in reader:
        print({y: row[y] for y in row.keys() if y})