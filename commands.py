"""commands"""

import sys

from prettytable import PrettyTable

from error import input_error
from constants import HELP, NUMBER_OF_CONTACTS_PER_PAGE
from address_book import Record, AddressBook
from fields import Phone


address_book = AddressBook()


def print_help(user_name: str) -> str:
    """Print help for the console bot program."""
    return f'{user_name}, this is help for the console bot program:\n{HELP}'


def help_from_bot(user_name) -> str:
    """Provide help from the bot."""
    return f'Greetings, {user_name}! How can I assist you today??'


@input_error
def add_contact(user_name: str, contact_name: str, phone_number: str) -> str:
    """Add a contact to the phone book."""

    if contact_name in address_book:
        raise ValueError(
            f"The contact '{contact_name.title()}' already exists in the address book.")
    phone = Phone(phone_number)
    contact = Record(contact_name)
    contact.add_phone_number(phone)
    address_book.add_record(contact)

    return f"{user_name}, the contact '{contact_name.title()}' has been added: {phone.phone}"


@input_error
def change_number_contact(user_name: str, contact_name: str, new_phone_number: str, old_phone_number: str) -> str:
    """Change the phone number of a contact in the phone book."""
    old_phone = Phone(old_phone_number)
    new_phone = Phone(new_phone_number)

    if contact_name not in address_book:
        raise KeyError(f"The contact '{contact_name.title()}' was not found.")

    contact = address_book.get_contact(contact_name)

    if old_phone not in contact.phone_numbers:
        raise ValueError(
            f"The contact's phone number '{old_phone.phone}' was not found in the address book.")

    if new_phone in contact.phone_numbers:
        raise ValueError(
            f"The contact's phone number '{new_phone.phone}' already exists in this '{contact_name.title()}' contact.")

    contact.edit_phone_number(old_phone, new_phone)
    address_book.add_record(contact)

    return f"{user_name}, the contact '{contact_name.title()}' has been updated with the new phone number: {new_phone.phone}"


@input_error
def print_contact(user_name: str, contact_name: str) -> str:
    """Print the phone number and other details of a contact from the phone book."""

    if contact_name not in address_book:
        raise KeyError(f"The contact '{contact_name.title()}' was not found.")

    table = PrettyTable()
    table.field_names = ["Contact name", "Phone number",
                         "Birthday", "Days to Birthday"]

    contact = address_book.get_contact(contact_name)
    phone_numbers = [number.phone for number in contact.phone_numbers]
    birthday = contact.birthday.birthday_date if contact.birthday else '-'
    day_to_birthday = contact.days_to_birthday()
    table.add_row([contact_name.title(), phone_numbers,
                  birthday, day_to_birthday])

    return f"{user_name}, '{contact_name.title()}':\n{table}"


@input_error
def delete_contact(user_name: str, contact_name: str) -> str:
    """Delete the phone number of a contact from the phone book."""

    if contact_name not in address_book:
        raise KeyError(f"The contact '{contact_name.title()}' was not found.")

    address_book.delete_record(contact_name)

    return f"{user_name}, the contact '{contact_name.title()}' has been deleted."


@input_error
def delete_contact_phone(user_name: str, contact_name: str, phone_number: str) -> str:
    """Deletes a phone number from an existing contact in the address book."""
    phone = Phone(phone_number)

    if contact_name not in address_book:
        raise KeyError(f"The contact '{contact_name.title()}' was not found.")

    contact = address_book.get_contact(contact_name)

    if phone not in contact.phone_numbers:
        raise ValueError(
            f"Contact's phone '{phone.phone}' was not found in the '{contact_name.title()}' contact.")

    contact.delete_phone_number(phone)

    return f"{user_name}, the phone number '{phone.phone}' was successfully deleted from the '{contact_name.title()}' contact."


@input_error
def add_number_phone_to_contact(user_name: str, contact_name: str, phone_number: str) -> str:
    """Adds a new phone number to an existing contact in the phone book."""
    phone = Phone(phone_number)

    if contact_name not in address_book:
        raise KeyError(f"The contact '{contact_name.title()}' was not found.")

    contact = address_book.get_contact(contact_name)

    if phone in contact.phone_numbers:
        raise ValueError(
            f"The phone number '{phone.phone}' already exists in the '{contact_name.title()}' contact.")

    contact.add_phone_number(phone)

    return f"{user_name}, the phone number '{phone.phone}' has been successfully added to the '{contact_name.title()}' contact."


@input_error
def print_all_contacts(user_name: str) -> str:
    """Print all contacts from the phone book."""

    for i, contacts in enumerate(address_book.record_iterator(NUMBER_OF_CONTACTS_PER_PAGE), 1):
        table = PrettyTable()
        table.field_names = ["Contact Name", "Phone Number",
                             "Birthday", "Days to Birthday"]

        for contact in contacts:
            contact_name = contact.name.name
            phone_numbers = [phone.phone for phone in contact.phone_numbers]
            birthday = contact.birthday.birthday_date if contact.birthday else '-'
            day_to_birthday = contact.days_to_birthday() if contact.birthday else '-'
            table.add_row(
                [contact_name.title(), phone_numbers, birthday, day_to_birthday])
        print(f"{user_name}, this is page {i} of your phone book:\n{table}")
    return "End of contacts."


@input_error
def add_birthday_date(user_name: str, contact_name: str, birthday_date) -> str:
    """Adds a birthday date to an existing contact in the phone book."""

    if contact_name not in address_book:
        raise KeyError(f"The contact '{contact_name.title()}' was not found.")

    contact = address_book.get_contact(contact_name)
    contact.add_birthday(birthday_date)
    address_book.add_record(contact)

    return f"{user_name}, the birthday '{birthday_date}' has been added to the '{contact_name.title()}' contact."


@input_error
def change_birthday_date(user_name: str, contact_name: str, new_birthday_date) -> str:
    """Changes the birthday date of an existing contact in the phone book."""

    if contact_name not in address_book:
        raise KeyError(f"The contact '{contact_name.title()}' was not found.")

    contact = address_book.get_contact(contact_name)
    contact.add_birthday(new_birthday_date)
    address_book.add_record(contact)
    return f"{user_name}, the birthday date for '{contact_name.title()}' has been changed to '{new_birthday_date}'."


def close_bot(contact_name: str):
    """Close the bot"""
    sys.exit(f'{contact_name}, Good bye!')
