import src.database as db
import time
import requests
import json

database = db.Client()
lst = database.list()

for line in lst:
    for word in line:
        if len(word.meaning) == 0:
            print(word.word)
            time.sleep(60)
            meaning = ""
            try:
                res = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word.word)
                res_dict = json.loads(res.text)
                if type(res_dict) == dict:
                    raise Exception(res_dict['message'])
                count = 0
                for m in res_dict[0]['meanings']:
                    pos = m['partOfSpeech']
                    meaning += "(" + pos + ") "
                    defs = m['definitions']
                    for d in defs:
                        count += 1
                        meaning += "| " + str(count) + ". " + d['definition'] + " "
                if len(meaning) == 0:
                    meaning = "N/A"
                database.update_entry(word.word, "meaning", meaning)
            except Exception as e:
                print("Cannot fetch meaning for {} because ".format(word), e)
