import requests
from codecs import open
from json import loads, dumps
from requests_oauthlib import OAuth1
from configparser import ConfigParser


class UiTdatabank():
    def __init__(self, settings_file="settings.cfg"):
        settings = ConfigParser()
        settings.read(settings_file)
        self.auth = OAuth1(settings["oauth"]["app_key"],
                           settings["oauth"]["app_secret"],
                           settings["oauth"]["user_token"],
                           settings["oauth"]["user_secret"])
        self.url = settings["uitdatabank"]["url"]
        self.headers = {'Accept': 'application/json'}

    def find(self, organiser_label=None):
        q = ''
        if organiser_label:
            q += 'organiser_label:' + organiser_label
        params = {'q': q, 'group': 'true'}
        r = requests.get(self.url, auth=self.auth, params=params, headers=self.headers)
        return loads(r.text)

if __name__ == '__main__':
    ud = UiTdatabank()
    flagey = ud.find(organiser_label="Flagey")
    with open("flagey.json", "w", "utf-8") as f:
        f.write(dumps(flagey, indent=2))
