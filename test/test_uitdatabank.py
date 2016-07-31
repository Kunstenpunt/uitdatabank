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

    def test_construct_event_query(self):
        single_field = [("title", "Hello world")]
        double_field_with_and = [("title", "Hello world"), "AND", ("city", "Brussel")]
        single_field_full_text = ["open air cinema"]
        wrong_list_because_no_boolean = [("title", "Hello world"), ("city", "Brussel")]
        wrong_list_because_no_valid_field = [("title", "Hello world"), ("foo", "bar")]
        self.assertEqual(self.udb.construct_event_query(single_field), "title:Hello world")
        self.assertEqual(self.udb.construct_event_query(double_field_with_and), "title:Hello world AND city:Brussel")
        self.assertEqual(self.udb.construct_event_query(single_field_full_text), "open air cinema")
        self.assertRaises(ValueError, self.udb.construct_event_query, wrong_list_because_no_boolean)
        self.assertRaises(ValueError, self.udb.construct_event_query, wrong_list_because_no_valid_field)

    def test_construct_query_parameters(self):
        good_parameters = {"q": "q"}
        bad_parameters = {"foo": "bar"}
        self.assertDictEqual(self.udb.construct_query_parameters(good_parameters), {"q": "q"})
        self.assertRaises(ValueError, self.udb.construct_query_parameters, bad_parameters)

if __name__ == '__main__':
    unittest.main()