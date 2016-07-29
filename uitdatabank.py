import requests
from codecs import open
from json import loads, dumps
from requests_oauthlib import OAuth1
from configparser import ConfigParser


class UiTdatabankSearchResults():
    def __init__(self, results_string):
        self.results = loads(results_string)


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

    def find(self, params):
        return requests.get(self.url, auth=self.auth, params=params, headers=self.headers).text

    def find_upcoming_events_by_organiser_label(self, organiser_label):
        q = 'organiser_label:' + organiser_label + ' AND availableto:[NOW TO *]'
        params = {'q': q, 'fq': 'type:event', 'group': 'event'}
        result = self.find(params)
        return UiTdatabankSearchResults(result)


if __name__ == '__main__':
    ud = UiTdatabank()
    flagey = ud.find_upcoming_events_by_organiser_label("Flagey")
    with open("flagey.json", "w", "utf-8") as f:
        f.write(dumps(flagey.results, indent=2))
