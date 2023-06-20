"""
This module provides functions for managing an address book and printing its contacts.

Functions:
    format_phone_number(func: Callable[..., str]) -> Callable[..., str]: 
                                                    A decorator function that adds a '+' sign to a phone number.
    sanitize_phone_number(phone: str) -> str: Cleans a phone number by removing unnecessary characters.
    print_all_contacts(addressbook: AB) -> str: Prints all the contacts in an address book in a formatted table.
"""

from typing import Callable
from prettytable import PrettyTable

from my_address_book.address_book import AddressBook as AB
from my_address_book.notes_book import NotesBook as NB


def format_phone_number(func: Callable[..., str]) -> Callable[..., str]:
    """
    Add '+' to phone's number
    """
    def add_code_phone(phone: str) -> str:
        phone = func(phone)
        return ''.join('+' + phone)

    return add_code_phone


@format_phone_number
def sanitize_phone_number(phone: str) -> str:
    """
    Clean number
    """
    return ''.join(number.strip().strip('(, ), -, +, x, .') for number in phone)


def print_all_contacts(addressbook: AB) -> str:
    """
    The print_all_contacts function prints all the contacts in the addressbook.
    It takes an AddressBook object as a parameter and returns nothing.

    :param addressbook: AB: Pass the addressbook object to the function
    """
    table = PrettyTable()
    phone_length = "Phone Number".ljust(20)
    emain_length = "Email".ljust(40)
    table.field_names = ["Contact Name", phone_length, emain_length, "Birthday", "Days to Birthday"]
    table.align["Contact Name"] = "l"
    table.align[phone_length] = "l"
    table.align[emain_length] = "l"

    for contact in addressbook.values():
        contact_name = contact.user.name

        phone_numbers: list[str] = []
        for number in contact.phone_numbers:
            if number.name:
                phone_numbers.append(number.subrecord.phone + f"({number.name[1]})")
            else:
                phone_numbers.append(number.subrecord.phone)
        if not phone_numbers:
            phone_numbers_for_table: str = '-'
        else:
            phone_numbers_for_table = '\n'.join(phone_numbers)

        emails: list[str] = []
        for email in contact.emails:
            if email.name:
                emails.append(email.subrecord.email + f"({email.name[1]})")
            else:
                emails.append(email.subrecord.email)
        if not emails:
            emails_for_table: str = '-'
        else:
            emails_for_table = '\n'.join(emails)

        birthday = contact.user.birthday_date.strftime('%d-%m-%Y') if contact.user.birthday_date else '-'

        day_to_birthday = contact.days_to_birthday() if contact.user.birthday_date else '-'

        table.add_row([contact_name, phone_numbers_for_table,
                      emails_for_table, birthday, day_to_birthday], divider=True)

    return str(table)


def print_all_notes(notesbook: NB) -> str:
    table = PrettyTable()
    note_length = "Note".ljust(80)
    table.field_names = ["#", "Note name", note_length, "Create date"]
    table.align["Note name"] = "l"
    table.align [note_length] = "l"
    table.align["Create date"] = "l"

    for key, record in notesbook.items():
        number_note_for_table = key
        name_note_for_table = record.note.name_note #if record.note.name_note else '-'
        note_for_table = record.note.note
        date_note_for_table = '\n'.join(str(record.date_of_creation).split())

        table.add_row([number_note_for_table, name_note_for_table, note_for_table, date_note_for_table], divider=True)

    return str(table)
