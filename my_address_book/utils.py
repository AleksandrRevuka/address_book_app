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
    table.field_names = ["Contact Name", "Phone Number", "Email", "Birthday", "Days to Birthday"]
    table.align["Contact Name"] = "l"
    table.align["Phone Number"] = "l"
    table.align["Email"] = "l"

    for contact in addressbook.values():
        contact_name = contact.user.name

        phone_numbers: list[str] = []
        for number in contact.phone_numbers:
            if number.subrecord.phone != '':
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
            if email.subrecord.email != '':
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

        table.add_row([contact_name.title(), phone_numbers_for_table,
                      emails_for_table, birthday, day_to_birthday], divider=True)

    return str(table)
