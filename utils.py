"""utils"""

from typing import Callable
from prettytable import PrettyTable

from address_book import  AddressBook as AB

def format_phone_number(func: Callable[..., str]) -> Callable[..., str]:
    """Add '+' to phone's number"""
    def add_code_phone(phone: str) -> str:
        phone = func(phone)
        return ''.join('+' + phone)

    return add_code_phone


@format_phone_number
def sanitize_phone_number(phone: str) -> str:
    """Clean number"""
    return ''.join(number.strip().strip('(, ), -, +, x, .') for number in phone)


def print_all_contacts(addressbook: AB) -> str:
    """
    The print_all_contacts function prints all the contacts in the addressbook.
        It takes an AddressBook object as a parameter and returns nothing.
    
    :param addressbook: AB: Pass the addressbook object to the function
    """
    table = PrettyTable()
    table.field_names = ["Contact Name", "Phone Number", "Email",
                            "Birthday", "Days to Birthday"]
    table.align["Contact Name"] = "l"
    table.align["Phone Number"] = "l"
    table.align["Email"] = "l"
    
    for contact in addressbook.values():
        contact_name = contact.user.name
        
        phone_numbers = '\n'.join([number.subrecord.phone for number in contact.phone_numbers if number.subrecord.phone != '']) or '-'
        
        emails = '\n'.join([email.subrecord.email for email in contact.emails if email.subrecord.email != '']) or '-'

        birthday = contact.user.birthday_date.strftime(
            '%d-%m-%Y') if contact.user.birthday_date else '-'
        
        day_to_birthday = contact.days_to_birthday() if contact.user.birthday_date else '-'

        table.add_row(
            [contact_name.title(), phone_numbers, emails, birthday, day_to_birthday], divider=True)

    return f"{table}"