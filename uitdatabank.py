import requests
from json import loads
from requests_oauthlib import OAuth1
from configparser import ConfigParser


class UiTdatabankSearchResults():
    def __init__(self, results_string):
        self.results = loads(results_string)

    def get_events(self):
        for item in self.results["rootObject"]:
            if "event" in item:
                yield {
                    "title": item["event"]["eventdetails"]["eventdetail"][0]["title"],
                    "description": item["event"]["eventdetails"]["eventdetail"][0]["longdescription"]
                }


class UiTdatabank():
    def __init__(self, settings_file="settings.cfg"):
        self.settings = ConfigParser()
        self.settings.read(settings_file)
        self.auth = OAuth1(self.settings["oauth"]["app_key"],
                           self.settings["oauth"]["app_secret"],
                           self.settings["oauth"]["user_token"],
                           self.settings["oauth"]["user_secret"])
        self.url = self.settings["uitdatabank"]["url"]
        self.headers = {'Accept': 'application/json'}

    def find(self, params):
        return requests.get(self.url, auth=self.auth, params=params, headers=self.headers).text

    def find_upcoming_events_by_organiser_label(self, organiser_label):
        q = 'organiser_label:' + organiser_label + ' AND startdate:[NOW TO *]'
        params = {'q': q, 'fq': 'type:event', 'group': 'event', 'rows': 10}
        result = self.find(params)
        return UiTdatabankSearchResults(result)
