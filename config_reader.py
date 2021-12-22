import json


def get_config():
    with open('config.json', 'r', encoding='UTF-8') as f:
        text = f.read()
    config = json.loads(text)
    return config
