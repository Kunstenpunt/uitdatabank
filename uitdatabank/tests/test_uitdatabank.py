import unittest

from uitdatabank.uitdatabank import UiTdatabank
from os.path import dirname


class TestUiTdatabank(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.udb = UiTdatabank(dirname(__file__) + "/settings_example.cfg", test=True)

    def test_construct_production_query(self):
        single_field = [("title", "Hello world")]
        double_field_with_and = [("title", "Hello world"), "AND", ("organiser_label", "Brussel")]
        single_field_full_text = ["open air cinema"]
        wrong_list_because_no_boolean = [("title", "Hello world"), ("organiser_label", "Brussel")]
        wrong_list_because_no_valid_field = [("title", "Hello world"), ("foo", "bar")]
        self.assertEqual(self.udb.construct_production_query(single_field), ("title:Hello world", "type:production"))
        self.assertEqual(self.udb.construct_production_query(double_field_with_and), ("title:Hello world AND organiser_label:Brussel", "type:production"))
        self.assertEqual(self.udb.construct_production_query(single_field_full_text), ("open air cinema", "type:production"))
        self.assertRaises(ValueError, self.udb.construct_production_query, wrong_list_because_no_boolean)
        self.assertRaises(ValueError, self.udb.construct_production_query, wrong_list_because_no_valid_field)

    def test_construct_event_query(self):
        single_field = [("title", "Hello world")]
        double_field_with_and = [("title", "Hello world"), "AND", ("city", "Brussel")]
        single_field_full_text = ["open air cinema"]
        double_field_boolean_fulltext = [("city", "Gent"), "AND", "jazz"]
        wrong_list_because_no_boolean = [("title", "Hello world"), ("city", "Brussel")]
        wrong_list_because_no_valid_field = [("title", "Hello world"), ("foo", "bar")]
        self.assertEqual(self.udb.construct_event_query(single_field), ("title:Hello world", "type:event"))
        self.assertEqual(self.udb.construct_event_query(double_field_with_and), ("title:Hello world AND city:Brussel", "type:event"))
        self.assertEqual(self.udb.construct_event_query(single_field_full_text), ("open air cinema", "type:event"))
        self.assertEqual(self.udb.construct_event_query(double_field_boolean_fulltext), ("city:Gent AND jazz", "type:event"))
        self.assertRaises(ValueError, self.udb.construct_event_query, wrong_list_because_no_boolean)
        self.assertRaises(ValueError, self.udb.construct_event_query, wrong_list_because_no_valid_field)

    def test_construct_query_parameters(self):
        good_parameters = {"q": "q"}
        bad_parameters = {"foo": "bar"}
        self.assertDictEqual(self.udb.construct_parameters_for_api_call(good_parameters), {"q": "q"})
        self.assertRaises(ValueError, self.udb.construct_parameters_for_api_call, bad_parameters)

    def test_q_parameter_examples(self):
        full_text = self.udb.construct_parameters_for_api_call({"q": "concert"})
        specific_field = self.udb.construct_parameters_for_api_call({"q": "city:Gent"})
        boolean_operator = self.udb.construct_parameters_for_api_call({"q": "cultuurcentrum AND berchem"})
        exact_term = self.udb.construct_parameters_for_api_call({"q": 'location_label:"cultuurcentrum berchem"'})
        self.assertLessEqual(len(self.udb.find(full_text).get_soonest_event()), 1)
        self.assertLessEqual(len(self.udb.find(specific_field).get_soonest_event()), 1)
        self.assertLessEqual(len(self.udb.find(boolean_operator).get_soonest_event()), 1)
        self.assertLessEqual(len(self.udb.find(exact_term).get_soonest_event()), 1)

    def test_fq_parameter_examples(self):
        concert_in_gent = self.udb.construct_parameters_for_api_call({"q": "concert", "fq": "city:Gent"})
        concert_in_gent_above_18 = self.udb.construct_parameters_for_api_call({"q": "concert", "fq": "city:Gent AND agefrom:18"})
        self.assertLessEqual(len(self.udb.find(concert_in_gent).get_soonest_event()), 1)
        self.assertLessEqual(len(self.udb.find(concert_in_gent_above_18).get_soonest_event()), 1)

if __name__ == '__main__':
    unittest.main()
