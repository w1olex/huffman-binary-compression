import unittest
import os
from src.kodovani import string_checker, vytvoreni_slozek


class TestStringMethods(unittest.TestCase):

    def test_string_checker(self):
        self.assertTrue(string_checker('abc123'))
        self.assertTrue(string_checker('ABC123'))
        self.assertFalse(string_checker('abc!@#'))
        self.assertFalse(string_checker('123!@#'))


    def test_vytvoreni_slozek(self):
        # Slozky tvořené do prarodičovských knihoven
        nazev_slozky = "test"
        expected_output = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), nazev_slozky)
        self.assertEqual(vytvoreni_slozek(nazev_slozky), expected_output)


if __name__ == '__main__':
    unittest.main()