import unittest
import os
from unittest.mock import patch

from src.kodovani import *

class TestKodovaciMetoda(unittest.TestCase):

    def test_kodovaci_metoda(self):

        encoded_data = kodovaci_metoda('test data', 'output_file.bin')
        self.assertIsInstance(encoded_data, str)


        with self.assertRaises(ValueError) as context:
            kodovaci_metoda(123, 'output_file.bin')
        self.assertEqual(str(context.exception), "Vstupní data musí být string.")


if __name__ == '__main__':
    unittest.main()