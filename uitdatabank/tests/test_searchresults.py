import unittest
from os.path import dirname, join
from re import compile, DOTALL
from json import dumps

from uitdatabank.shortcuts import Shortcuts


class TestSearchResults(unittest.TestCase):
    def setUp(self):
        udbsc = Shortcuts(join(dirname(__file__), "settings_example.cfg"), True)
        self.searchresults = udbsc.find_upcoming_events_by_organiser_label("Flagey")
        self.raw_results = dumps(self.searchresults.results)

    def test_get_events_has_expected_length(self):
        events = list(self.searchresults.get_events())
        self.assertEqual(len(events), 10)

    def test_get_when_from_event(self):
        regex = compile('"calendar":\s\{.+?(\d{13}).+?\}', DOTALL)
        lowest_timestamp = min([int(date) for date in regex.findall(self.raw_results)])
        self.assertIn(str(lowest_timestamp), dumps(self.searchresults.get_soonest_event()["event"]["calendar"]))

if __name__ == '__main__':
    unittest.main()
