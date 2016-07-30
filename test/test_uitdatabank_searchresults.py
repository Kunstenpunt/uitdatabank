import unittest
from codecs import open
from uitdatabank import UiTdatabankSearchResults


class TestUiTdatabankSearchResults(unittest.TestCase):
    def setUp(self):
        with open("test_output_of_upcoming_events_query.json", "r", "utf-8") as f:
            self.searchresults = UiTdatabankSearchResults(f.read())

    def test_get_events(self):
        events = list(self.searchresults.get_events())
        self.assertEquals(len(events), 10)

if __name__ == '__main__':
    unittest.main()