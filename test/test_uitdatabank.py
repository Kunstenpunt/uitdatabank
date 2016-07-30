import unittest
from uitdatabank import UiTdatabank


class TestUiTdatabank(unittest.TestCase):
    def setUp(self):
        self.udb = UiTdatabank("../settings_example.cfg")

    def test_settings_are_read_in_correctly(self):
        self.assertEqual(self.udb.settings["oauth"]["app_key"], "BAAC107B-632C-46C6-A254-13BC2CE19C6C")
        self.assertEqual(self.udb.settings["oauth"]["app_secret"], "ec9a0e8c2cdc52886bc545e14f888612")

if __name__ == '__main__':
    unittest.main()