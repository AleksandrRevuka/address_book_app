"""address book"""

from datetime import datetime
from collections import UserDict
from fields import Name, Phone, Birthday


class AddressBook(UserDict):
    """ A class that represents an address book containing contact records."""

    def get_contact(self, name):
        """Returns the contact record for the given name."""
        return self.data[name]

    def add_record(self, record):
        """Adds a new contact record to the address book."""
        self.data[record.name.name] = record

    def delete_record(self, record_name):
        """Removes a contact record from the address book."""
        del self.data[record_name]

    def record_iterator(self, n):
        """Returns a generator that yields N records at a time."""
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i+n]

    def search(self):
        """Searches the address book for contacts matching the given criteria."""
        pass


class Record:
    """ A class that represents a contact record in a phone book."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday_data = None

    def add_phone(self, phone):
        """Adds a new phone number to the contact."""
        self.phones.append(Phone(phone))

    def edit_phone(self, phone_number, new_phone_number):
        """Updates an existing phone number for the contact."""
        for phone in self.phones:
            if phone.phone == phone_number:
                phone.phone = new_phone_number
                break

    def delete_phone(self, phone_number):
        """Removes a phone number from the contact."""
        for phone in self.phones:
            if phone.phone == phone_number:
                self.phones.remove(phone)
                break

    def add_birthday_data(self, birthday_data):
        """Add a birthday data to the contact."""
        self.birthday_data = Birthday(birthday_data)

    def days_to_birthday(self):
        """Calculate the number of days to the next birthday."""
        if self.birthday_data:
            now = datetime.now()
            birthday = self.birthday_data.birthday_data
            next_birthday = datetime(now.year, birthday.month, birthday.day)
            if next_birthday < now:
                next_birthday = datetime(
                    now.year + 1, birthday.month, birthday.day)

            return (next_birthday - now).days
        return '-'
