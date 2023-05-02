"""Tests class Name"""
import unittest

from fields import Name


class TestName(unittest.TestCase):
    """Tests class Name"""

    def setUp(self) -> None:
        self.name_test = Name('Sasha')

    def tearDown(self) -> None:
        del self.name_test

    def test_name(self):
        """
        The test_name function tests the name attribute of the Name class.
        It does this by creating a new instance of the Name class, and then using
        the assertEquals method to test that it is equal to 'Sasha'. If it is not,
        then an error will be thrown.
        """
        self.assertEqual(self.name_test.name, 'Sasha')

    def test_set_name(self):
        """
        The test_set_name function tests the set_name function in Name.py
        It does this by setting a name to 'Pasha' and then checking if it is equal to 'Pasha'.
        If it is, then the test passes.
        """
        self.name_test.name = 'Pasha'
        self.assertEqual(self.name_test.name, 'Pasha')

    def test_verify_name(self):
        """
        The test_verify_name function tests the Name class's name property.
        The function raises a TypeError if the new_name variable is not a string, and raises a 
        ValueError if it is an empty string or longer than 50 characters.
        """
        with self.assertRaises(TypeError) as error:
            self.name_test.name = 12
        self.assertTrue('Name must be a string, but got' in str(error.exception))

        with self.assertRaises(TypeError) as error:
            new_name = 'Sasha1986'
            self.name_test.name = new_name
        self.assertTrue(
            f"Contact's name can only contain letters, but got '{new_name.title()}'", str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.name_test.name = ''
        self.assertTrue('Name length must be between' in str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.name_test.name = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.assertTrue('Name length must be between' in str(error.exception))


if __name__ == '__main__':
    unittest.main()