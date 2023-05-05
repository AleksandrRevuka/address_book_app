"""address book"""

import re
import pickle
from datetime import datetime
from collections import UserDict
from entities import Phone, User, Email


class AddressBook(UserDict):
    """A class that represents an address book containing contact records."""

    def get_contact(self, name: str) -> User:
        """Returns the contact record for the given name."""
        return self.data[name]

    def add_record(self, record):
        """Adds a new contact record to the address book."""
        self.data[record.user.name] = record
        self.sort_addressbook()

    def delete_record(self, record_name: str):
        """Removes a contact record from the address book."""
        del self.data[record_name]

    def record_iterator(self, count_elements: int):
        """Returns a generator that yields N records at a time."""
        records = list(self.data.values())
        for i in range(0, len(records), count_elements):
            yield records[i:i+count_elements]

    def sort_addressbook(self):
        """The sort_addressbool function sorts the address book by name."""
        self.data = dict(sorted(self.data.items(), key=lambda x: x[0]))

    def search(self, criteria: str):
        """Searches the address book for contacts matching the given criteria."""
        serch_contacts = AddressBook()

        if criteria.isdigit():
            for record in self.data.values():
                for phone_number in record.phone_numbers:
                    if re.search(criteria, phone_number.subrecord.phone):
                        serch_contacts.add_record(record)

        else:
            for record in self.data.values():
                if re.search(criteria, record.user.name):
                    serch_contacts.add_record(record)
                
        if len(serch_contacts) == 0:
            return f"According to this '{criteria}' criterion, no matches were found"
        
        return serch_contacts

    def save_records_to_file(self, file_name: str):
        """Save the data in the address book to a binary file using pickle."""
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def read_records_from_file(self, file_name: str):
        """Read data from a binary file using pickle and update the address book."""
        try:
            with open(file_name, "rb") as file:
                content = pickle.load(file)
                self.data.update(content)
        except FileNotFoundError as error:
            raise f"File not found {file_name}" from error


class Record:
    """A class that represents a contact record in a phone book."""
    class Subrecord:
        """..."""
        def __init__(self, subrecord, name_subrecord='basic'):
            self.name = name_subrecord
            self.subrecord = subrecord
            

    def __init__(self, user: User):
        self.user = user
        self.phone_numbers = []
        self.emails = []

    def add_phone_number(self, phone_number: Phone):
        """Adds a new phone number to the contact."""
        subrecord_phone = self.Subrecord(phone_number)
        self.phone_numbers.append(subrecord_phone)
        
    def add_email(self, email: Email):
        """Adds a new email to the contact."""
        subrecord_email = self.Subrecord(email)
        self.emails.append(subrecord_email)

    def edit_phone_number(self, old_phone_number: Phone, new_phone_number: Phone):
        """Updates an existing phone number for the contact."""
        for phone_number in self.phone_numbers:
            if phone_number.subrecord == old_phone_number:
                phone_number.subrecord.phone = new_phone_number.phone
                break
            
    def edit_email(self, old_email: Email, new_email: Email):
        """Updates an existing phone number for the contact."""
        for email in self.emails:
            if email.subrecord == old_email:
                email.subrecord.email = new_email.email
                break

    def delete_phone_number(self, phone_number: Phone):
        """Removes a phone number from the contact."""
        for i, number in enumerate(self.phone_numbers):
            if number.subrecord == phone_number:
                del self.phone_numbers[i]
                break
            
    def delete_email(self, del_email: Email):
        """Removes a phone number from the contact."""
        for i, email in enumerate(self.emails):
            if email.subrecord == del_email:
                del self.emails[i]
                break

    def add_birthday(self, birthday_date: str):
        """Add a birthday data to the contact."""
        self.user.birthday_date = birthday_date

    def days_to_birthday(self, current_date=None):
        """Calculate the number of days to the next birthday."""
        if current_date is None:
            current_date = datetime.now()

        birthday = self.user.birthday_date
        next_birthday = datetime(current_date.year, birthday.month, birthday.day)

        if next_birthday < current_date:
            next_birthday = datetime(
                current_date.year + 1, birthday.month, birthday.day)

        return (next_birthday - current_date).days
