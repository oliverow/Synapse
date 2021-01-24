import csv
import src.database as db
import time

input_file = open('similar.csv', 'r')
reader = csv.reader(input_file)

client = db.Client()

for line in reader:
    words = list(filter(lambda e: len(e)>0, line[1:]))
    print(words)
    first_word = words.pop(0)
    client.create_entry(first_word.strip(), "")
    for word in words:
        time.sleep(1)
        client.create_entry(word.strip(), "", {"word": first_word.strip()})
    time.sleep(1)
