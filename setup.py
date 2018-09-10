import json

host = input("host: ")

owners = []

TOKEN = input("token: ")

description = input("desc: ")

prefix = input("prefix: ")

toogleall = 0

invite_link = input("invite: ")

config = {'host': host, 'owners': owners, 'token': TOKEN, 'desc': description, 'prefix': prefix, 'logall': toogleall, 'invite': invite_link}

with open('config.json', 'w') as f:
    json.dump(config, f)
