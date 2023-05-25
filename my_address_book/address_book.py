"""Address book"""

import re
import pickle
from datetime import datetime
from typing import Union, Any, List
from collections import UserDict

from my_address_book.entities import Phone, User, Email


class AddressBook(UserDict):
    """A class that represents an address book containing contact records."""

    def get_contact(self, name: str) -> 'Record':
        """Returns the contact record for the given name."""
        return self.data[name]

    def add_record(self, record: 'Record') -> None:
        """Adds a new contact record to the address book."""
        name = record.user.name
        if name:
            self.data[name.lower()] = record
            self.sort_addressbook()

    def delete_record(self, record_name: str) -> None:
        """Removes a contact record from the address book."""
        del self.data[record_name]

    def sort_addressbook(self) -> None:
        """The sort_addressbook function sorts the address book by name."""
        self.data = dict(sorted(self.data.items(), key=lambda x: x[0]))

    def search(self, criteria: str) -> Union[str, 'AddressBook']:
        """Searches the address book for contacts matching the given criteria."""
        search_contacts = AddressBook()

        if criteria.isdigit():
            for record in self.data.values():
                for phone_number in record.phone_numbers:
                    if re.search(criteria, phone_number.subrecord.phone):
                        search_contacts.add_record(record)

        else:
            for name, record in self.data.items():
                if re.search(criteria, name):
                    search_contacts.add_record(record)

        if len(search_contacts) == 0:
            return f"According to this '{criteria}' criterion, no matches were found"

        return search_contacts

    def save_records_to_file(self, file_name: str) -> None:
        """Save the data in the address book to a binary file using pickle."""
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def read_records_from_file(self, file_name: str) -> None:
        """Read data from a binary file using pickle and update the address book."""
        try:
            with open(file_name, "rb") as file:
                content = pickle.load(file)
                self.data.update(content)
        except FileNotFoundError as error:
            raise FileNotFoundError(f"File not found {file_name}") from error


class Record:
    """A class that represents a contact record in a phone book."""

    class Subrecord:
        """..."""

        def __init__(self, subrecord: Any, name_subrecord: list | None):
            self.name = name_subrecord
            self.subrecord = subrecord

    def __init__(self, user: User):
        self.user = user
        self.phone_numbers: List['Record.Subrecord'] = []
        self.emails: List['Record.Subrecord'] = []

    def add_phone_number(self, phone_number: Phone, phone_assignment: list | None = None) -> None:
        """Adds a new phone number to the contact."""
        subrecord_phone = self.Subrecord(phone_number, phone_assignment)
        self.phone_numbers.append(subrecord_phone)

    def add_email(self, email: Email, email_assignment: list | None = None) -> None:
        """Adds a new email to the contact."""
        subrecord_email = self.Subrecord(email, email_assignment)
        self.emails.append(subrecord_email)

    def add_birthday(self, birthday_date: datetime) -> None:
        """Add a birthday data to the contact."""
        self.user.birthday_date = birthday_date

    def days_to_birthday(self, current_date: Union[datetime, None] = None) -> Union[int, None]:
        """Calculate the number of days to the next birthday."""
        if current_date is None:
            current_date = datetime.now()

        birthday = self.user.birthday_date
        if birthday is None:
            return None

        next_birthday = datetime(current_date.year, birthday.month, birthday.day)

        if next_birthday < current_date:
            next_birthday = datetime(
                current_date.year + 1, birthday.month, birthday.day)

        return (next_birthday - current_date).days
