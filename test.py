import requests
from codecs import open
from json import loads, dumps
from requests_oauthlib import OAuth1
from sys import argv

if argv[1] == "update":

  url = 'https://www.uitid.be/uitid/rest/searchv2/search'

  auth = OAuth1('BAAC107B-632C-46C6-A254-13BC2CE19C6C', 'ec9a0e8c2cdc52886bc545e14f888612', '', '')

  headers = {'Accept': 'application/json'}
  params  = {'q': 'organiser_label:Flagey', 'group':'true'}

  r = requests.get(url, auth=auth, params=params, headers=headers)
  with open("flagey.json", "w", "utf-8") as f:
    f.write(dumps(loads(r.text), indent=2))

with open("flagey.json", "r", "utf-8") as f:
  docs = loads(f.read())
