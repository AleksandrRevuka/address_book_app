"""Test class AddressBook"""
import os
import pickle
import unittest
from datetime import datetime

from my_address_book.address_book import AddressBook as AB
from my_address_book.entities import Email
from my_address_book.entities import Phone
from my_address_book.entities import User
from my_address_book.records import RecordContact


class TestAddressBook(unittest.TestCase):
    """Tests class AddressBook"""

    def setUp(self) -> None:
        self.addressbook_test = AB()
        self.user_test = User("sasha")
        self.phone_test = Phone("380951234567")
        self.email_test = Email("test_sasha@gmail.com")
        self.record_test = RecordContact(self.user_test)
        self.record_test.add_birthday(datetime(1982, 6, 26))
        self.record_test.add_phone_number(self.phone_test)
        self.record_test.add_email(self.email_test)

        current_dir = os.getcwd()
        self.test_file = os.path.join(current_dir, "tests", "test_file.bin")

    def tearDown(self) -> None:
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        del self.addressbook_test
        del self.record_test
        del self.user_test
        del self.phone_test
        del self.email_test

    def test_get_contact_and_add_record(self) -> None:
        """
        The test_get_contact_and_add_record function tests the get_contact function in AddressBook.py
        by adding a record to an address book and then retrieving it by name.
        """
        self.addressbook_test.add_record(self.record_test)
        contact: RecordContact = self.addressbook_test.get_record("sasha")
        self.assertEqual(contact.user.name, "sasha")

    def test_delete_record(self) -> None:
        """
        The test_delete_record function tests the delete_record function in AddressBook.py
            by adding a record to an address book and then deleting it. It checks that the
            record is no longer in the address book.
        """
        self.addressbook_test.add_record(self.record_test)
        self.addressbook_test.delete_record("sasha")
        self.assertFalse("sasha" in self.addressbook_test)

    def test_search_name(self) -> None:
        """
        The test_search_name function tests the search function in AddressBook.py
            by adding a record to an addressbook and then searching for that record.
            The test passes if the name of the contact is found in the search results.
        """
        self.addressbook_test.add_record(self.record_test)
        addressbook_search = self.addressbook_test.search("sa")
        self.assertTrue("sasha" in addressbook_search)

    def test_search_birthday(self) -> None:
        """
        The test_search_birthday function tests the search function in AddressBook.py
            by searching for a birthday that is present in the addressbook_test object,
            and checking if it returns an object with &quot;sasha&quot; as one of its keys.
        """
        self.addressbook_test.add_record(self.record_test)
        addressbook_search = self.addressbook_test.search("26-06")
        self.assertTrue("sasha" in addressbook_search)

    def test_search_email(self) -> None:
        """
        The test_search_email function tests the search function in AddressBook.py
            by adding a record to an addressbook and then searching for that record's email.
            The test passes if the email is found.
        """

        self.addressbook_test.add_record(self.record_test)
        addressbook_search = self.addressbook_test.search("gmail.com")
        if isinstance(addressbook_search, AB):
            contact: RecordContact = addressbook_search.get_record("sasha")
        record_email = contact.emails[0].subrecord.email
        self.assertTrue("gmail.com" in record_email)

    def test_search_phone(self) -> None:
        """
        The test_search_phone function tests the search function of the AddressBook class.
        It creates a contact, adds a phone number to it and then adds this contact to an addressbook.
        Then it searches for all contacts with 38095 in their phone numbers and checks if there is at
        least one such record.
        """

        self.addressbook_test.add_record(self.record_test)
        addressbook_search = self.addressbook_test.search("38095")
        if isinstance(addressbook_search, AB):
            contact: RecordContact = addressbook_search.get_record("sasha")
        record_phone = contact.phone_numbers[0].subrecord.phone
        self.assertTrue("380951234567" in record_phone)

    def test_search_future_birthday(self) -> None:
        """
        The test_search_future_birthday function tests the search function in AddressBook.py
            to see if it can find a record with a birthday that is in the future.
            The test_search_future_birthday function takes no parameters and returns None.
        """

        self.addressbook_test.add_record(self.record_test)
        addressbook_search = self.addressbook_test.search("-0")
        self.assertTrue(0 == len(addressbook_search))

    def test_search_past_birthday(self) -> None:
        """
        The test_search_past_birthday function tests the search function in AddressBook.py
            to see if it can find a record that has a birthday more than 365 days ago.
            The test_search_past_birthday function is called by the unittest module, and
            uses assertTrue to check if the length of addressbook_search is 0.
        """

        self.addressbook_test.add_record(self.record_test)
        addressbook_search = self.addressbook_test.search("+365")
        self.assertTrue(0 == len(addressbook_search))

    def test_search_none(self) -> None:
        """
        The test_search_none function tests the search function in AddressBook.py
            to see if it returns an empty list when there is no match for the inputted string.
        """

        self.addressbook_test.add_record(self.record_test)
        addressbook_search = self.addressbook_test.search("1111")
        self.assertTrue(0 == len(addressbook_search))

    def test_save_records_to_file(self) -> None:
        """
        The test_save_records_to_file function tests the save_records_to_file function in AddressBook.py
            by adding a record to an address book and then saving it to a file. The test then opens the file,
            loads its contents into memory, and checks that the name of one of the records is present.
        """
        self.addressbook_test.add_record(self.record_test)

        self.addressbook_test.save_records_to_file(self.test_file)

        with open(self.test_file, "rb") as file:
            content = pickle.load(file)
            self.assertTrue("sasha" in content)

    def test_read_records_from_file(self) -> None:
        """
        The test_read_records_from_file function tests the read_records_from_file function in AddressBook.py
            by creating a test file, adding a record to it, and then reading that record from the file into
            an addressbook object. The test passes if 'Sasha' is in the addressbook object.
        """
        with open(self.test_file, "wb") as file:
            self.addressbook_test.add_record(self.record_test)
            pickle.dump(self.addressbook_test, file)

        self.addressbook_test.read_records_from_file(self.test_file)

        self.assertTrue("sasha" in self.addressbook_test)

    def test_read_records_from_file_file_not_found(self) -> None:
        """
        The test_read_records_from_file_FileNotFound function tests the read_records_from_file function in
        AddressBook.py to ensure that it raises a FileNotFoundError when an invalid file name is passed to it.
        """

        file_name = "invalid_file"

        with self.assertRaises(FileNotFoundError) as error:
            self.addressbook_test.read_records_from_file(file_name)
        self.assertEqual(f"File not found {file_name}", str(error.exception))


if __name__ == "__main__":
    unittest.main()
