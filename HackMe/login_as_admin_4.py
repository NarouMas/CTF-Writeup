import requests

url = 'https://ctf.hackme.quest/login4/'
post = {'name': 'admin'}
ret = requests.post(url, post, allow_redirects=False)
print(ret.text)