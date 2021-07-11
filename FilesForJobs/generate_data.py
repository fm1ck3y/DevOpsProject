import requests
import sys
import random

if len(sys.argv) < 3:
    exit()

N = int(sys.argv[1])
HOST = sys.argv[2]

if 'http://' not in HOST or 'https://' not in HOST:
    HOST = 'http://' + HOST

NAMES = ["Artem Vdovin", "Igor Lepeyko"]
EMAILS = ["123@mail.ru","456@mail.ru"]
USERNAMES = ["llll123", "mmmm3333"]
INFORMATIONS = ["PRIVET","POKA"]
PASSWORDS = ["123","hi"]


for i in range(N):
    user = f'{{"email" : "{random.choice(EMAILS)}","username":"{random.choice(USERNAMES)}","full_name" : "{random.choice(NAMES)}",' \
           f'"information_bio" : "{random.choice(INFORMATIONS)}","password" : "{random.choice(PASSWORDS)}"}}'
    print(f"{HOST}/api/v1.0/add_user?user={user}")
    response = requests.get(url = f"{HOST}/api/v1.0/add_user?user={user}")
