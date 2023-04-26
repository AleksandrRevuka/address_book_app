"""address book"""

from datetime import datetime
from collections import UserDict
from fields import Name, Birthday


class AddressBook(UserDict):
    """A class that represents an address book containing contact records."""

    def get_contact(self, name):
        """Returns the contact record for the given name."""
        return self.data[name]

    def add_record(self, record):
        """Adds a new contact record to the address book."""
        self.data[record.name.name] = record

    def delete_record(self, record_name):
        """Removes a contact record from the address book."""
        del self.data[record_name]

    def record_iterator(self, num_elements):
        """Returns a generator that yields N records at a time."""
        records = list(self.data.values())
        for i in range(0, len(records), num_elements):
            yield records[i:i+num_elements]

    def search(self):
        """Searches the address book for contacts matching the given criteria."""
        pass


class Record:
    """A class that represents a contact record in a phone book."""

    def __init__(self, name):
        self.name = Name(name)
        self.phone_numbers = []
        self.birthday = None

    def add_phone_number(self, phone_number):
        """Adds a new phone number to the contact."""
        self.phone_numbers.append(phone_number)

    def edit_phone_number(self, old_phone_number, new_phone_number):
        """Updates an existing phone number for the contact."""
        for phone_number in self.phone_numbers:
            if phone_number == old_phone_number:
                phone_number.phone = new_phone_number.phone
                break

    def delete_phone_number(self, phone_number):
        """Removes a phone number from the contact."""
        for i, number in enumerate(self.phone_numbers):
            if number == phone_number:
                del self.phone_numbers[i]
                break

    def add_birthday(self, birthday_date):
        """Add a birthday data to the contact."""
        self.birthday = Birthday(birthday_date)

    def days_to_birthday(self):
        """Calculate the number of days to the next birthday."""
        now = datetime.now()
        birthday = self.birthday.birthday_date
        next_birthday = datetime(now.year, birthday.month, birthday.day)
        if next_birthday < now:
            next_birthday = datetime(
                now.year + 1, birthday.month, birthday.day)

        return (next_birthday - now).days
