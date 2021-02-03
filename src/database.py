from neo4j import GraphDatabase
import requests
import json
import re

from src.word import Word

class Client:
    def __init__(self):
        uri = "bolt://localhost:7687"
        driver = GraphDatabase.driver(uri, auth=("synapase", "1129"))
        self.session = driver.session()

    def __del__(self):
        self.session.close()

    def list(self):
        res = self.session.run("match(w:word)-[:similar]->(y:word) return y, collect(w)")
        lines = []
        for result in res.data():
            line = [result['y']] + result['collect(w)']
            lines.append(list(map(lambda x: Word(x), line)))
        res = self.session.run("match(w:word) where not (w)-[:similar]-(:word) return w")
        for result in res.data():
            lines.append([Word(result['w'])])
        return lines

    def create_entry(self, word, hint, similar=None):
        meaning = ""
        try:
            res = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+word)
            res_dict = json.loads(res.text)
            count = 0
            for m in res_dict[0]['meanings']:
                pos = m['partOfSpeech']
                meaning += "(" + pos + ") "
                defs = m['definitions']
                for d in defs:
                    count += 1
                    meaning += "| " + str(count) + ". " + d['definition'] + " "
        except Exception as e:
            print("Cannot fetch meaning for {} because ".format(word), e)

        if similar is None:
            command = "create(w:word {word:\""+word+"\", meaning: $meaning, hint:\""+hint+"\", wrongtimes:1, memorized:false, starred:false})"
        else:
            command = "match(w:word {word:\""+similar.word+"\"}) create(y:word {word:\""+word+"\", meaning: $meaning, hint:\""+hint+"\", wrongtimes:1, memorized:false, starred:false})-[:similar]->(w)"

        try:
            res = self.session.run(command, meaning=meaning)
        except Exception as e:
            print("Database operation failed")
            print(e)
        return "Complete"

    def update_entry(self, word, prop_name, value):
        command = "match(w:word {word:\""+word+"\"}) set w."+prop_name+"=$value"
        try:
            res = self.session.run(command, value=value)
        except Exception as e:
            print("Database operation failed")
            print(e)
        return "Complete"
