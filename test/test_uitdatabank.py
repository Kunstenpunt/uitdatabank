import unittest
from uitdatabank import UiTdatabank
from json import dumps
from codecs import open


class TestUiTdatabank(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.udb = UiTdatabank("../settings_example.cfg", test=True)
        cls.events = cls.udb.find_upcoming_events_by_organiser_label(organiser_label="Flagey")

    def test_settings_are_read_in_correctly(self):
        self.assertEqual(self.udb.settings["oauth"]["app_key"], "BAAC107B-632C-46C6-A254-13BC2CE19C6C")
        self.assertEqual(self.udb.settings["oauth"]["app_secret"], "ec9a0e8c2cdc52886bc545e14f888612")

    def test_find_upcoming_events_by_organiser_label(self):
        events = self.udb.find_upcoming_events_by_organiser_label(organiser_label="Flagey")
        with open("test_output_of_upcoming_events_query.json", "w", "utf-8") as f:
            f.write(dumps(events.results, indent=2))

if __name__ == '__main__':
    unittest.main()