"""Test class Record"""
import os
import pickle
import unittest
from fields import Phone
from address_book import AddressBook, Record

class TestRecord(unittest.TestCase):
    """Tests class Record"""

    def setUp(self) -> None:
        self.addressbook_test = AddressBook()
        self.contact_test = Record('Sasha')
        self.phone_test = Phone('380951234567')
        current_dir = os.getcwd()
        self.test_file = os.path.join(current_dir, 'tests', 'test_file.bin')

    def tearDown(self) -> None:
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        del self.addressbook_test
        del self.contact_test

    def test_get_contact_and_add_record(self):
        """
        The test_get_contact_and_add_record function tests the get_contact function in AddressBook.py
        by adding a record to an address book and then retrieving it by name.
        """
        self.addressbook_test.add_record(self.contact_test)
        contact = self.addressbook_test.get_contact('Sasha')
        self.assertEqual(contact.name.name, 'Sasha')

    def test_delete_record(self):
        """
        The test_delete_record function tests the delete_record function in AddressBook.py
            by adding a record to an address book and then deleting it. It checks that the
            record is no longer in the address book.
        """
        self.addressbook_test.add_record(self.contact_test)
        self.addressbook_test.delete_record('Sasha')
        self.assertFalse('Sasha' in self.addressbook_test)

    def test_search_name(self):
        """
        The test_search_name function tests the search function in AddressBook.py
            by adding a record to an addressbook and then searching for that record.
            The test passes if the name of the contact is found in the search results.
        """
        self.addressbook_test.add_record(self.contact_test)
        addressbook_search = self.addressbook_test.search('Sa')
        self.assertTrue('Sasha' in addressbook_search)

    def test_search_phone(self):
        """
        The test_search_phone function tests the search function of the AddressBook class.
        It creates a contact, adds a phone number to it and then adds this contact to an addressbook.
        Then it searches for all contacts with 38095 in their phone numbers and checks if there is at least one such record.
        """
        contact = self.contact_test
        contact.add_phone_number(self.phone_test)
        self.addressbook_test.add_record(contact)
        addressbook_search = self.addressbook_test.search('38095')
        contact = addressbook_search.get_contact('Sasha')
        record = contact.phone_numbers[0]
        self.assertTrue('380951234567' in record.phone)

    def test_search_nothing(self):
        """
        The test_search_nothing function tests the search function in AddressBook.py
            by adding a record to an addressbook and then searching for a string that is not present in the record.
            The test passes if it returns 'According to this'
        """
        self.addressbook_test.add_record(self.contact_test)
        addressbook_search = self.addressbook_test.search('Pa')
        self.assertTrue('According to this' in addressbook_search)

    def test_save_records_to_file(self):
        """
        The test_save_records_to_file function tests the save_records_to_file function in AddressBook.py
            by adding a record to an address book and then saving it to a file. The test then opens the file,
            loads its contents into memory, and checks that the name of one of the records is present.
        """
        self.addressbook_test.add_record(self.contact_test)
        
        self.addressbook_test.save_records_to_file(self.test_file)
        
        with open(self.test_file, 'rb') as file:
            content = pickle.load(file)
            self.assertTrue('Sasha' in content)
            
    def test_read_records_from_file(self):
        """
        The test_read_records_from_file function tests the read_records_from_file function in AddressBook.py
            by creating a test file, adding a record to it, and then reading that record from the file into an addressbook object.
            The test passes if 'Sasha' is in the addressbook object.
        """  
        with open(self.test_file, 'wb') as file:
            self.addressbook_test.add_record(self.contact_test)
            pickle.dump(self.addressbook_test, file)

        self.addressbook_test.read_records_from_file(self.test_file)
        
        self.assertTrue('Sasha' in self.addressbook_test)
        