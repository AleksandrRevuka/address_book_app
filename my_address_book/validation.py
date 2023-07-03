"""
This module provides functions for validating and checking various input parameters related to an address book.

Functions:

    name_validation(name: str) -> None: Verifies that a given name is a valid name for a contact.
    phone_validation(phone: str) -> None: Verifies that a given phone number is valid.
    birthday_date_validation(birthday_date: datetime) -> None: Verifies that a given birthday date is valid.
    email_validation(email: str) -> None: Verifies that a given email address is valid.
    check_name_in_address_book(address_book: AB, name: str) -> None:
                                                            Checks if a given name already exists in the address book.
    check_name_not_in_address_book(address_book: AB, name: str) -> None:
                                                            Checks if a given name does not exist in the address book.
    check_number_not_in_notes_book(notes_book: NB, number: str) -> None:
                                                            Checks if the number is in the notes book.
"""
import re
import os
from datetime import date
from datetime import datetime
from pathlib import Path
from string import digits

from my_address_book.address_book import AddressBook as AB
from my_address_book.constants import LETTERS
from my_address_book.constants import NAME_RANGE
from my_address_book.constants import NOTE_LEN
from my_address_book.constants import PHONE_RANGE
from my_address_book.error import input_error
from my_address_book.notes_book import NotesBook as NB


@input_error
def name_validation(name: str) -> None:
    """
    Verifies that the input string `name` is a valid name for a contact.
    """

    if not isinstance(name, str):
        raise TypeError(f"Name must be a string, but got {type(name).__name__}")

    if len(name.strip(LETTERS)) != 0:
        raise TypeError(f"Contact's name can only contain letters, but got '{name.title()}'")

    if len(name) not in NAME_RANGE:
        raise ValueError(f"Name length must be between {NAME_RANGE[0]} and {NAME_RANGE[-1]}, but got '{name.title()}'")


@input_error
def phone_validation(phone: str) -> None:
    """
    Verifies a phone number.
    """

    if len(phone.strip(digits + "+")) != 0:
        raise TypeError(f"Contact's phone can only contain digits, but got '{phone}'")

    if len(phone) not in PHONE_RANGE:
        raise ValueError(f"Contact's phone must be between 11 and 16 numbers, but got '{phone}'")


@input_error
def birthday_date_validation(birthday_date: date) -> None:
    """
    Verifies a birthday date.
    """
    if isinstance(birthday_date, date):
        if birthday_date >= datetime.now().date():
            raise ValueError(f"Birthday '{birthday_date}' must be in the past")


@input_error
def email_validation(email: str) -> None:
    """
    Verifies an email address.
    """
    pattern = r"[a-zA-Z][a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    if not re.match(pattern, email):
        raise ValueError(f"Invalid '{email}' email address.")


@input_error
def note_validation(note: str) -> None:
    """
    The note_validation function checks if the length of a note is more than NOTE_LEN.
    If it's not, then an error will be raised.
    """

    if len(note) < NOTE_LEN:
        raise ValueError(f"Note length must be more {NOTE_LEN}, but got '{note}'")


@input_error
def check_name_in_address_book(address_book: AB, name: str) -> None:
    """
    The check_name_in_address_book function checks if a name is already in the address book.
        If it is, then an error message will be raised.
    """
    if name in (name_contact for name_contact in address_book):
        raise ValueError(f"The contact '{name}' already exists in the address book.")


@input_error
def check_name_not_in_address_book(address_book: AB, name: str) -> None:
    """
    The check_name_not_in_address_book function checks if the name is already in the address book.
        If it is, then a ValueError exception will be raised with an error message explaining that
        the contact already exists in the address book.
    """
    if name not in (name_contact for name_contact in address_book):
        raise KeyError(f"The contact {name} was not found.")


@input_error
def check_number_not_in_notes_book(notes_book: NB, number: str) -> None:
    """
    The check_number_not_in_notes_book function checks if the number is in the notes book.
    If it is not, then a KeyError will be raised.
    """

    if number not in (number_note for number_note in notes_book):
        raise KeyError(f"The note {number} was not found.")


@input_error
def check_path_address_to_sort_files_in_it(path: Path) -> None:
    """Checks if the path (for sorting files) exists and if it points to a folder"""
    if not path.exists():
        raise ValueError("The way is not exists!")
    if os.path.isfile(path):
        raise ValueError("The path points to a file! Must point to a folder!")
