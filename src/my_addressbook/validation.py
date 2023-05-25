"""validation"""

import re
from string import digits
from datetime import datetime

from my_addressbook.error import input_error
from my_addressbook.constants import LETTERS, NAME_RANGE, PHONE_RANGE
from my_addressbook.address_book import AddressBook as AB


@input_error
def name_validation(name: str) -> None:
    """Verifies that the input string `name` is a valid name for a contact."""

    if not isinstance(name, str):
        raise TypeError(
            f"Name must be a string, but got {type(name).__name__}")

    if len(name.strip(LETTERS)) != 0:
        raise TypeError(
            f"Contact's name can only contain letters, but got '{name.title()}'")

    if len(name) not in NAME_RANGE:
        raise ValueError(
            f"Name length must be between {NAME_RANGE[0]} and {NAME_RANGE[-1]}, but got '{name.title()}'")


@input_error
def phone_validation(phone: str) -> None:
    """Verifies a phone number."""

    if len(phone.strip(digits + '+')) != 0:
        raise TypeError(
            f"Contact's phone can only contain digits, but got '{phone}'")

    if len(phone) not in PHONE_RANGE:
        raise ValueError(
            f"Contact's phone must be between 11 and 16 numbers, but got '{phone}'")


@input_error
def birthday_date_validation(birthday_date: datetime) -> None:
    """Verifies a birthday data."""
    if isinstance(birthday_date, datetime):
        if birthday_date >= datetime.now().date():
            raise ValueError(
                f"Birthday '{birthday_date}' must be in the past")


@input_error
def email_validation(email: str) -> None:
    """Verifies an email address."""
    pattern = r"[a-zA-Z][a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    if not re.match(pattern, email):
        raise ValueError(f"Invalid '{email}' email address.")


@input_error
def criteria_validation(criteria: str) -> None:
    """
    The verify_criteria function is used to verify that the criteria entered by the user
    is only numbers or letters.  If it is not, then a ValueError exception will be raised.
    """
    if not criteria.isdigit() and not criteria.isalpha():
        raise ValueError(
            f"Criteria '{criteria}' must be only numbers or letters")


@input_error
def check_name_in_address_book(address_book: AB, name: str) -> None:
    """
    The check_name_in_address_book function checks if a name is already in the address book.
        If it is, then an error message will be raised.
    """
    name.lower()
    if name in (name.lower() for name in address_book):
        raise ValueError(
            f"The contact '{name.title()}' already exists in the address book.")


@input_error
def check_name_not_in_address_book(address_book: AB, name: str) -> None:
    """
    The check_name_not_in_address_book function checks if the name is already in the address book.
        If it is, then a ValueError exception will be raised with an error message explaining that
        the contact already exists in the address book.
    """
    name = name.lower()
    if name not in (name.lower() for name in address_book):
        raise KeyError(f"The contact '{name.title()}' was not found.")

