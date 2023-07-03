"""
The address_book module provides classes for managing an address book and contact records.

This module defines the following classes:
    - AddressBook: A class representing an address book containing contact records.
    - Record: A class representing a contact record in the address book.
"""
import re

from my_address_book.constants import PUNCTUATION
from my_address_book.interface_book import Book
from my_address_book.records import RecordContact


class AddressBook(Book):
    """
    A class that represents an address book containing contact records.

    Methods:
        add_record(record: 'Record') -> None:
            Adds a new contact record to the address book.
        search(criteria: str) -> Union[str, 'AddressBook']:
            Searches the address book for contacts matching the given criteria.
    """

    def add_record(self, record: "RecordContact") -> None:
        """
        Adds a new contact record to the address book.
        """
        name = record.user.name
        if name:
            self.data[name] = record
            self.sort_book()

    def search(self, criteria: str) -> "AddressBook":
        """
        Searches the address book for contacts matching the given criteria.
        """
        search_contacts = AddressBook()

        for record in self.data.values():
            if self._matches_criteria(record, criteria):
                search_contacts.add_record(record)

        return search_contacts

    def _matches_criteria(self, record: "RecordContact", criteria: str) -> bool:
        """
        Checks if a contact record matches the given search criteria.
        """
        if criteria[0] not in PUNCTUATION:
            if re.search(criteria.lower(), record.user.name.lower()):
                return True

            if record.user.birthday_date and re.search(criteria, record.user.birthday_date.strftime("%d-%m-%Y")):
                return True

            if any(re.search(criteria, phone.subrecord.phone) for phone in record.phone_numbers):
                return True

            if any(re.search(criteria.lower(), email.subrecord.email.lower()) for email in record.emails):
                return True

        if record.days_to_birthday() is not None:
            if criteria[0] == "-" and criteria[1:].isdigit():
                return int(criteria[1:]) >= record.days_to_birthday()

            if criteria[0] == "+" and criteria[1:].isdigit():
                return int(criteria[1:]) <= record.days_to_birthday()

        return False
