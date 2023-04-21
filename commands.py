"""commands"""

import sys

from prettytable import PrettyTable

from error import input_error
from constants import HELP
from address_book import Record, AddressBook


phone_book = AddressBook()


def print_help(your_name: str) -> str:
    """Print help for the console bot program."""
    return f'{your_name}, This is help for the console bot program:\n{HELP}'


def help_from_bot(your_name) -> str:
    """Provide help from the bot."""
    return f'{your_name}, How can I help you?'


@input_error
def add_contact(your_name: str, name: str, phone: str) -> str:
    """Add a contact to the phone book."""
    
    if name in phone_book:
        raise ValueError(f"Contact '{name.title()}' exists in the address book")

    contact = Record(name)
    contact.add_phone(phone)
    phone_book.add_record(contact)

    return f"{your_name}, contact has been added '{name.title()}': {phone}"

 
@input_error
def change_number_contact(your_name: str, name: str, phone: str, old_phone: str) -> str:
    """Change the phone number of a contact in the phone book."""

    if name not in phone_book:
        raise KeyError(f"Contact '{name.title()}' not found")

    contact = phone_book.get_contact(name)
    contact_numbers = [number.value for number in contact.phones]

    if old_phone not in contact_numbers:
        raise ValueError(f"Contact's phone '{old_phone}' not found in the address book")
    
    if phone in contact_numbers:
        raise ValueError(f"Contact's phone '{phone}' exists in this '{name.title()}' contact")

    contact.edit_phone(old_phone, phone)
    phone_book.add_record(contact)

    return f"{your_name}, contact has been changed '{name.title()}': {phone}"


@input_error
def print_number_contact(your_name: str, name: str) -> str:
    """Print the phone number of a contact from the phone book."""

    if name not in phone_book:
        raise KeyError(f"Contact '{name.title()}' not found")
    
    contact = phone_book.get_contact(name)
    contact_numbers = [number.value for number in contact.phones]

    return f"{your_name}, This contact '{name.title()}' has phone number: '{contact_numbers}' "


@input_error
def delete_contact(your_name: str, name: str) -> str:
    """Delete the phone number of a contact from the phone book."""

    if name not in phone_book:
        raise KeyError(f"Contact {name.title()} not found")
    
    phone_book.delete_record(name)

    return f"{your_name}, This contact {name.title()} has been deleted"


@input_error
def delete_contact_phone(your_name: str, name: str, phone: str) -> str:
    """Deletes a phone number from an existing contact in the address book."""

    if name not in phone_book:
        raise KeyError(f"Contact '{name.title()}' not found")
    
    contact = phone_book.get_contact(name)
    contact_numbers = [number.value for number in contact.phones]

    if phone not in contact_numbers:
        raise ValueError(f"Contact's phone '{phone}' not found in this '{name.title()}' contact")

    contact.delete_phone(phone)

    return f"{your_name}, Contact's phone '{phone}' was deleted from the-s '{name.title()}' contact"


@input_error
def add_number_phone_to_contact(your_name: str, name: str, phone: str) -> str:
    """Adds a new phone number to an existing contact in the phone book."""

    if name not in phone_book:
        raise KeyError(f"Contact {name.title()} not found")

    contact = phone_book.get_contact(name)
    contact_numbers = [number.value for number in contact.phones]

    if phone in contact_numbers:
        raise ValueError(f"Contact's phone '{phone}' exists in this '{name.title()}' contact")

    contact.add_phone(phone)

    return f"{your_name}, '{name.title()}'s' new contact phone number '{phone}' has been successfully added to the address book"


def print_all_contacts(your_name: str) -> str:
    """Print all contacts from the phone book."""

    table = PrettyTable()
    table.field_names = ["Name contact", "number phone"]

    for contact in phone_book.values():
        name = contact.name.value
        phones = [phone.value for phone in contact.phones]
        table.add_row([name.title(), phones])

    return f"{your_name}, This is your phone book:\n{table}"


def close_bot(name: str):
    """Close the bot"""
    sys.exit(f'{name}, Good bye!')
