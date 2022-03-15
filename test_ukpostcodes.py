import unittest
from uk_postcodes import *


class TestPostcodes(unittest.TestCase):
    def test_isValid(self):

        #valid normal cases:
        valid_cases = ["EC1A 1BB", "W1A 0AX", "M1 1AE", "B33 8TH", "CR2 6XH", "DN55 1PT", "dn551pt", "dn551pt   "]
        for i in valid_cases:
            self.assertTrue(ValidatePostcode(i).func_validate_postcode())

        #invalid outward Cases:
        invalid_outward = ["BR11 9YY", "BR12 9YY", "BR13 9YY    "]
        for i in invalid_outward:
            with self.assertRaises(InvalidOutward):
                ValidatePostcode(i).func_validate_postcode()

        #invalid inward Cases:
        invalid_inward = ["BR1 9CI", "BR1 9KM"]
        for i in invalid_inward:
            with self.assertRaises(InvalidInward):
                ValidatePostcode(i).func_validate_postcode()

        #invalid postcode cases:
        invalid_postcode = ["-1","1234", "DV 00"]
        for i in invalid_postcode:
            with self.assertRaises(InvalidPostcode):
                ValidatePostcode(i).func_validate_postcode()

        #Value Error Cases:
        value_error = ["", " "]
        for i in value_error:
            with self.assertRaises(ValueError):
                ValidatePostcode(i).func_validate_postcode()

        #Special Cases:
        special_cases = ["ASCN 1ZZ", "AI-2640", "KY1-1001", "DV 05"]
        for i in special_cases:
            self.assertTrue(ValidatePostcode(i).func_validate_postcode())


if __name__ == '__main__':
    unittest.main()