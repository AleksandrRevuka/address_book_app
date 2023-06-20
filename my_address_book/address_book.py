"""
The address_book module provides classes for managing an address book and contact records.

This module defines the following classes:
    - AddressBook: A class representing an address book containing contact records.
    - Record: A class representing a contact record in the address book.
"""

import re
from typing import Union
from abc import ABC, abstractmethod

from my_address_book.interface_book import Book
from my_address_book.records import RecordContact
from my_address_book.constants import PUNCTUATION


class IAddressBook(ABC):
    """Interface AddressBook"""

    @abstractmethod
    def add_record(self, record: RecordContact):
        pass

    @abstractmethod
    def search(self, criteria: str):
        pass


class AddressBook(Book, IAddressBook):
    """
    A class that represents an address book containing contact records.

    Methods:
        add_record(record: 'Record') -> None:
            Adds a new contact record to the address book.
        search(criteria: str) -> Union[str, 'AddressBook']:
            Searches the address book for contacts matching the given criteria.
    """

    def add_record(self, record: 'RecordContact') -> None:
        """
        Adds a new contact record to the address book.
        """
        name = record.user.name
        if name:
            self.data[name] = record
            self.sort_book()

    def search(self, criteria: str) -> Union[str, 'AddressBook']:
        """
        Searches the address book for contacts matching the given criteria.
        """
        search_contacts = AddressBook()

        if criteria[0] not in PUNCTUATION:
            for record in self.data.values():
                if re.search(criteria.lower(), record.user.name.lower()):
                    search_contacts.add_record(record)
                    
                if record.user.birthday_date:
                    if re.search(criteria, record.user.birthday_date.strftime('%d-%m-%Y')):
                        search_contacts.add_record(record)
                        
                    if re.search(criteria, str(record.days_to_birthday())):
                        search_contacts.add_record(record)
                    
                for phone_number in record.phone_numbers:
                    if re.search(criteria, phone_number.subrecord.phone):
                        search_contacts.add_record(record)
                        
                for email in record.emails:
                    if re.search(criteria.lower(), email.subrecord.email.lower()):
                        search_contacts.add_record(record)
                        
        if criteria[0] == "-" and criteria[1:].isdigit():
            for record in self.data.values():
                if int(criteria[1:]) >= record.days_to_birthday():
                    search_contacts.add_record(record)
                    
        if criteria[0] == "+" and criteria[1:].isdigit():
            for record in self.data.values():
                if int(criteria[1:]) <= record.days_to_birthday():
                    search_contacts.add_record(record)
                    
        return search_contacts
