import requests
from json import loads
from requests_oauthlib import OAuth1
from configparser import ConfigParser
from datetime import datetime, timedelta


class UiTdatabankSearchResults():
    def __init__(self, results_string):
        self.results = loads(results_string)

    @staticmethod
    def _get_when_from_event(event):
        """
        Fetches the dates and hours at which the event starts
        :param event: the 'event' json document that is produced by the UiTdatabank v2 api
        :return: a list of python datetime objects indicating at what day and hour the event starts
        """
        return [datetime.fromtimestamp(ts["date"] / 1000.) + timedelta(milliseconds=ts["timestart"], hours=1)
                for ts in event["event"]["calendar"]["timestamps"]["timestamp"]]


    def get_events(self):
        for item in self.results["rootObject"]:
            if "event" in item and item["event"]["eventdetails"]["eventdetail"][0]["longdescription"]:
                yield {
                    "title": item["event"]["eventdetails"]["eventdetail"][0]["title"],
                    "description": item["event"]["eventdetails"]["eventdetail"][0]["longdescription"],
                    "when": self._get_when_from_event(item)
                }


class UiTdatabank():
    def __init__(self, settings_file="settings_example.cfg", test=False):
        self.settings = ConfigParser()
        self.test = test
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
        params = {'q': q, 'fq': 'type:event', 'group': False, 'rows': 10 if self.test else 10000}
        return UiTdatabankSearchResults(result)
