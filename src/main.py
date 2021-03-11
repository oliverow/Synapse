from src.app import gui_app
from src.database import Client
from src.initialization import initialization_app
import json
import subprocess
import os


CONFIG_FILE = 'config.json'

def main():
    config_obj = read_config()
    init = initialization_app(config_obj)
    init_completed = init.check_complete()
    if not init_completed: init.mainloop()
    write_config(config_obj)
    client = Client()
    app = gui_app(client)
    app.mainloop()
    wrap_up(config_obj)

def read_config():
    with open(CONFIG_FILE, 'r+') as config_file:
        config_obj = json.load(config_file)
    return config_obj

def write_config(config_obj):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_obj, config_file)

def wrap_up(config_obj):
    db_path = config_obj['neo4j_path']
    result = subprocess.check_output('cd \"{}\"; ./neo4j stop'.format(os.path.normpath(db_path)), stderr = subprocess.STDOUT, shell = True)
    print(result)

if __name__ == '__main__':
    main()
