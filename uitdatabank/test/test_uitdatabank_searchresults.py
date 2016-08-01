import unittest
from codecs import open
from uitdatabank.uitdatabank import UiTdatabankSearchResults
from os.path import dirname


class TestUiTdatabankSearchResults(unittest.TestCase):
    def setUp(self):
        with open(dirname(__file__) + "/test_output_of_upcoming_events_query.json", "r", "utf-8") as f:
            self.searchresults = UiTdatabankSearchResults(f.read())

    def test_get_events_has_expected_length(self):
        events = list(self.searchresults.get_events())
        self.assertEqual(len(events), 10)

if __name__ == '__main__':
    unittest.main()