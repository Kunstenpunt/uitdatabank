import unittest
from codecs import open
from uitdatabank.uitdatabank import UiTdatabankSearchResults
from os.path import dirname
from re import compile, DOTALL
from json import dumps


class TestUiTdatabankSearchResults(unittest.TestCase):
    def setUp(self):
        with open(dirname(__file__) + "/test_output_of_upcoming_events_query.json", "r", "utf-8") as f:
            self.raw_results = f.read()
            self.searchresults = UiTdatabankSearchResults(self.raw_results)

    def test_get_events_has_expected_length(self):
        events = list(self.searchresults.get_events())
        self.assertEqual(len(events), 10)

    def test_get_when_from_event(self):
        regex = compile('"calendar":\s\{.+?(\d{13}).+?\}', DOTALL)
        lowest_timestamp = min([int(date) for date in regex.findall(self.raw_results)])
        self.assertIn(str(lowest_timestamp), dumps(self.searchresults.get_soonest_event()["event"]["calendar"]))

if __name__ == '__main__':
    unittest.main()
