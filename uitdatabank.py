import requests
from codecs import open
from json import loads, dumps
from requests_oauthlib import OAuth1


class UiTdatabank():
    def __init__(self, app_key, app_secret, user_token, user_secret, url):
        self.auth = OAuth1(app_key, app_secret, user_token, user_secret)
        self.url = url
        self.headers = {'Accept': 'application/json'}

    def find(self, organiser_label=None):
        q = ''
        if organiser_label:
            q += 'organiser_label:' + organiser_label
        params = {'q': q, 'group': 'true'}
        r = requests.get(self.url, auth=self.auth, params=params, headers=self.headers)
        return loads(r.text)

if __name__ == '__main__':
    ud = UiTdatabank('BAAC107B-632C-46C6-A254-13BC2CE19C6C', 'ec9a0e8c2cdc52886bc545e14f888612', '', '',
                     'https://www.uitid.be/uitid/rest/searchv2/search')
    flagey = ud.find(organiser_label="Flagey")
    with open("flagey.json", "w", "utf-8") as f:
        f.write(dumps(flagey, indent=2))
