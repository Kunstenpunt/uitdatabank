import unittest
from codecs import open
from uitdatabank import UiTdatabankSearchResults
from datetime import datetime


class TestUiTdatabankSearchResults(unittest.TestCase):
    def setUp(self):
        with open("test_output_of_upcoming_events_query.json", "r", "utf-8") as f:
            self.searchresults = UiTdatabankSearchResults(f.read())

    def test_get_events_has_expected_length(self):
        events = list(self.searchresults.get_events())
        self.assertEqual(len(events), 10)

    def test_get_when_from_item(self):
        for item in self.searchresults.results["rootObject"]:
            if "event" in item and item["event"]["eventdetails"]["eventdetail"][0]["longdescription"]:
                calendarstr = item["event"]["eventdetails"]["eventdetail"][0]["calendarsummary"]
                when = self.searchresults._get_when_from_event(item)
                if len(when) == 1:
                    day, month, year = [int(i) for i in calendarstr.split(" ")[1].split("/")]
                    hour, minute = [int(i) for i in calendarstr.split(" ")[3].split(":")]
                    self.assertEqual(min(when), datetime(2000 + year, month, day, hour, minute))

if __name__ == '__main__':
    unittest.main()