#unit_tests.py
import unittest
import sys
sys.path.append("src")
from logic.reverse_mortgage import ReverseMortgageCalculator

from logic.exceptions import  (
    DataTypeError,
    InvalidPropertyValueError,
    ExcessivePropertyValueError,
    InvalidInterestRateError,
    InvalidPropertyConditionError,
    InvalidMaritalStatusError,
    InvalidInputError
)


class TestReverseMortgageCalculator(unittest.TestCase):

    # Normal Cases: Tests with typical scenarios

    def test_Normal_1(self):
        calculator = ReverseMortgageCalculator(
            property_value=500000000,
            property_condition="excellent",
            marital_status="married",
            owner_age=70,
            spouse_age=68,
            interest_rate=0.5
        )
        expected_payment = 1041666.67
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Normal_2(self):
        calculator = ReverseMortgageCalculator(
            property_value=400000000,
            property_condition="good",
            marital_status="married",
            owner_age=72,
            spouse_age=70,
            interest_rate=0.5
        )
        expected_payment = 1000000
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Normal_3(self):
        calculator = ReverseMortgageCalculator(
            property_value=250000000,
            property_condition="average",
            marital_status="married",
            owner_age=65,
            spouse_age=67,
            interest_rate=0.07
        )
        expected_payment = 416666.67
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Normal_4(self):
        calculator = ReverseMortgageCalculator(
            property_value=300000000,
            property_condition="average",
            marital_status="married",
            owner_age=70,
            spouse_age=68,
            interest_rate=0.5
        )
        expected_payment = 500000
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Normal_5(self):
        calculator = ReverseMortgageCalculator(
            property_value=300000000,
            property_condition="excellent",
            marital_status="married",
            owner_age=75,
            spouse_age=65,
            interest_rate=0.06
        )
        expected_payment = 625000
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Normal_6(self):
        calculator = ReverseMortgageCalculator(
            property_value=280000000,
            property_condition="good",
            marital_status="married",
            owner_age=80,
            spouse_age=70,
            interest_rate=0.08
        )
        expected_payment = 700000
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    # Extraordinary Cases: Tests with edge cases and unusual scenarios

    def test_Extraordinary_1(self):
        calculator = ReverseMortgageCalculator(
            property_value=650000000,
            property_condition="good",
            marital_status="married",
            owner_age=90,
            spouse_age=85,
            interest_rate=0.05
        )
        expected_payment = 1625000
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Extraordinary_2(self):
        calculator = ReverseMortgageCalculator(
            property_value=300000000,
            property_condition="excellent",
            marital_status="married",
            owner_age=80,
            spouse_age=18,
            interest_rate=0.07
        )
        expected_payment = 500000
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Extraordinary_3(self):
        calculator = ReverseMortgageCalculator(
            property_value=500000000,
            property_condition="excellent",
            marital_status="married",
            owner_age=70,
            spouse_age=68,
            interest_rate=0.0001
        )
        expected_payment = 1041666.67
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Extraordinary_4(self):
        calculator = ReverseMortgageCalculator(
            property_value=200000000,
            property_condition="excellent",
            marital_status="married",
            owner_age=70,
            spouse_age=70,
            interest_rate=0.07
        )
        expected_payment = 555555.56
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Extraordinary_5(self):
        calculator = ReverseMortgageCalculator(
            property_value=500000000,
            property_condition="good",
            marital_status="married",
            owner_age=70,
            spouse_age=85,
            interest_rate=0.07
        )
        expected_payment = 1250000
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    def test_Extraordinary_6(self):
        calculator = ReverseMortgageCalculator(
            property_value=900000000,
            property_condition="average",
            marital_status="married",
            owner_age=70,
            spouse_age=65,
            interest_rate=0.1
        )
        expected_payment = 1500000
        result = calculator.calculate_monthly_payment()
        self.assertEqual(round(result, 2), expected_payment)

    # Error Cases: Tests that expect exceptions

    def test_Error_1(self):
        with self.assertRaises(DataTypeError):
            ReverseMortgageCalculator(
                property_value="",
                property_condition="excellent",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=0.07
            ).calculate_payment()

    def test_Error_2(self):
        with self.assertRaises(InvalidPropertyValueError):
            ReverseMortgageCalculator(
                property_value=0,
                property_condition="excellent",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=0.07
            ).calculate_monthly_payment()

    def test_Error_3(self):
        with self.assertRaises(ExcessivePropertyValueError):
            ReverseMortgageCalculator(
                property_value=1000000000,
                property_condition="excellent",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=0.04
            ).calculate_monthly_payment()

    def test_Error_4(self):
        with self.assertRaises(InvalidInterestRateError):
            ReverseMortgageCalculator(
                property_value=400000000,
                property_condition="excellent",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=0
            ).calculate_monthly_payment()

    def test_Error_5(self):
        with self.assertRaises(InvalidPropertyConditionError):
            ReverseMortgageCalculator(
                property_value=300000000,
                property_condition="unknown",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=0.07
            ).calculate_monthly_payment()

    def test_Error_6(self):
        with self.assertRaises(InvalidMaritalStatusError):
            ReverseMortgageCalculator(
                property_value=500000000,
                property_condition="excellent",
                marital_status="",
                owner_age=70,
                spouse_age=68,
                interest_rate=0.07
            ).calculate_monthly_payment()

    def test_Error_7(self):
        with self.assertRaises(DataTypeError):
            ReverseMortgageCalculator(
                property_value="300000000O",
                property_condition="good",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=0.07
            ).calculate_payment()

    def test_Error_8(self):
        with self.assertRaises(InvalidMaritalStatusError):
            ReverseMortgageCalculator(
                property_value=300000000,
                property_condition="excellent",
                marital_status=None,
                owner_age=70,
                spouse_age=68,
                interest_rate=0.07
            ).calculate_monthly_payment()

    def test_Error_9(self):
        with self.assertRaises(InvalidInterestRateError):
            ReverseMortgageCalculator(
                property_value=400000000,
                property_condition="excellent",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=2  # Invalid interest rate
            ).calculate_monthly_payment()

    def test_Error_10(self):
        with self.assertRaises(ExcessivePropertyValueError):
            ReverseMortgageCalculator(
                property_value=950000000,
                property_condition="excellent",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=0.07
            ).calculate_monthly_payment()

    def test_Error_11(self):
        with self.assertRaises(ExcessivePropertyValueError):
            ReverseMortgageCalculator(
                property_value=950000000,
                property_condition="excellent",
                marital_status="married",
                owner_age=70,
                spouse_age=68,
                interest_rate=0.07
            ).calculate_monthly_payment()

if __name__ == '__main__':
    unittest.main()


