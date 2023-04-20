"""address book"""

from collections import UserDict
from fields import Name, Phone


class AddressBook(UserDict):
    """ A class that represents an address book containing contact records."""

    def get_contact(self, name):
        """Returns the contact record for the given name."""
        return self.data[name]
    
    def add_record(self, record):
        """Adds a new contact record to the address book."""
        self.data[record.name.value] = record
    
    def delete_record(self, record_name):
        """Removes a contact record from the address book."""
        del self.data[record_name]
    
    def search(self):
        """Searches the address book for contacts matching the given criteria."""
        pass


class Record:
    """ A class that represents a contact record in a phone book."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Adds a new phone number to the contact."""
        self.phones.append(Phone(phone))
    
    def edit_phone(self, phone_number, new_phone_number):
        """Updates an existing phone number for the contact."""
        for phone in self.phones:
            if phone.value == phone_number:
                phone.value = new_phone_number
                break
    
    def delete_phone(self, phone_number):
        """Removes a phone number from the contact."""
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break
