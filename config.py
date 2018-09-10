import json

with open('config.json', 'r') as f:
    config = json.load(f)

host = config['host']

owners = config['owners']

TOKEN = config['token']

description = config['desc']

prefix = config['prefix']

toogleall = config['logall']

invite_link = config['invite']
