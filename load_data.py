import requests

link = r'https://fantasy.premierleague.com/api/bootstrap-static/'

r = requests.get(link)

j_son = r.json()
with open('fantasy.json', 'w') as json_file:
    json_file.write(j_son)
    
