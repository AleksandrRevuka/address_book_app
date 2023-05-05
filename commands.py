"""commands"""

import sys

from prettytable import PrettyTable

from error import input_error
from constants import HELP, NUMBER_OF_CONTACTS_PER_PAGE
from address_book import Record, AddressBook as AB
from entities import Phone, User


# address_book = AddressBook()


def print_help(user_name: str) -> str:
    """Print help for the console bot program."""
    return f'{user_name}, this is help for the console bot program:\n{HELP}'


@input_error
def add_contact(
        address_book: AB,
        user_name: str,
        contact_name: str,
        phone_number: str) -> str:
    """Add a contact to the phone book."""
    if contact_name and phone_number:
        if contact_name in address_book:
            raise ValueError(
                f"The contact '{contact_name.title()}' already exists in the address book.")
        phone = Phone(phone_number)
        user = User(contact_name)
        contact = Record(user)
        contact.add_phone_number(phone)
        address_book.add_record(contact)
    else:
        return "After the command, you must enter the new contact's name and phone number separated by a space.\nFor example: 'Smith 380631234567'"
    
    return f"{user_name}, the contact '{contact_name.title()}' has been added: {phone.phone}"


@input_error
def change_number_contact(
        address_book: AB,
        user_name: str,
        contact_name: str,
        new_phone_number: str,
        old_phone_number: str) -> str:
    """Change the phone number of a contact in the phone book."""
    if contact_name and new_phone_number and old_phone_number:

        old_phone = Phone(old_phone_number)
        new_phone = Phone(new_phone_number)

        if contact_name not in address_book:
            raise KeyError(f"The contact '{contact_name.title()}' was not found.")

        contact = address_book.get_contact(contact_name)

        if old_phone not in [phone_number.subrecord for phone_number in contact.phone_numbers]:
            raise ValueError(
                f"The contact's phone number '{old_phone.phone}' was not found in the address book.")

        if new_phone in [phone_number.subrecord for phone_number in contact.phone_numbers]:
            raise ValueError(
                f"The contact's phone number '{new_phone.phone}' already exists in this '{contact_name.title()}' contact.")

        contact.edit_phone_number(old_phone, new_phone)
        address_book.add_record(contact)

    else:
        return "After the command, you must enter the existing contact's name, the new phone number, and the old phone number, separated by spaces.\nFor example: 'Smith 380631234567 380956785434'"

    return f"{user_name}, the contact '{contact_name.title()}' has been updated with the new phone number: {new_phone.phone}"


@input_error
def print_contact(
        address_book: AB,
        user_name: str,
        contact_name: str) -> str:
    """Print the phone number and other details of a contact from the phone book."""
    if contact_name:

        if contact_name not in address_book:
            raise KeyError(f"The contact '{contact_name.title()}' was not found.")

        table = PrettyTable()
        table.field_names = ["Contact name", "Phone number", "Email", "Birthday", "Days to Birthday"]

        contact = address_book.get_contact(contact_name)
        phone_numbers = [number.subrecord.phone for number in contact.phone_numbers]
        emails = [email.subrecord.email for email in contact.emails]
        birthday = contact.user.birthday_date if contact.user.birthday_date else '-'
        day_to_birthday = contact.days_to_birthday() if contact.user.birthday_date else '-'
        table.add_row([contact_name.title(), phone_numbers, emails, birthday, day_to_birthday])
    else:
        return "After the command, you must enter the existing contact's name.\nFor example: 'Smith'"

    return f"{user_name}, '{contact_name.title()}':\n{table}"


@input_error
def delete_contact(
        address_book: AB,
        user_name: str,
        contact_name: str) -> str:
    """Delete the phone number of a contact from the phone book."""
    if contact_name:
        if contact_name not in address_book:
            raise KeyError(f"The contact '{contact_name.title()}' was not found.")

        address_book.delete_record(contact_name)
    else:
        return "After the command, you must enter the existing contact's name.\nFor example: 'Smith'"

    return f"{user_name}, the contact '{contact_name.title()}' has been deleted."


@input_error
def delete_contact_phone(
        address_book: AB,
        user_name: str,
        contact_name: str,
        phone_number: str) -> str:
    """Deletes a phone number from an existing contact in the address book."""
    if contact_name and phone_number:
        phone = Phone(phone_number)

        if contact_name not in address_book:
            raise KeyError(f"The contact '{contact_name.title()}' was not found.")

        contact = address_book.get_contact(contact_name)

        if phone not in [phone_number.subrecord for phone_number in contact.phone_numbers]:
            raise ValueError(
                f"Contact's phone '{phone.phone}' was not found in the '{contact_name.title()}' contact.")

        contact.delete_phone_number(phone)
    else:
        return "After the command, you must enter the existing contact's name and phone number separated by a space.\nFor example: 'Smith 380631234567'"

    return f"{user_name}, the phone number '{phone.phone}' was successfully deleted from the '{contact_name.title()}' contact."


@input_error
def add_number_phone_to_contact(
        address_book: AB,
        user_name: str,
        contact_name: str,
        phone_number: str) -> str:
    """Adds a new phone number to an existing contact in the phone book."""
    if contact_name and phone_number:
        phone = Phone(phone_number)

        if contact_name not in address_book:
            raise KeyError(f"The contact '{contact_name.title()}' was not found.")

        contact = address_book.get_contact(contact_name)

        if phone in [phone_number.subrecord for phone_number in contact.phone_numbers]:
            raise ValueError(
                f"The phone number '{phone.phone}' already exists in the '{contact_name.title()}' contact.")

        contact.add_phone_number(phone)
    else:
        return "After the command, you must enter the existing contact's name and new phone number separated by a space.\nFor example: 'Smith 380631234567'"

    return f"{user_name}, the phone number '{phone.phone}' has been successfully added to the '{contact_name.title()}' contact."


@input_error
def print_all_contacts(address_book: AB, user_name: str) -> str:
    """Print all contacts from the phone book."""

    for i, contacts in enumerate(address_book.record_iterator(NUMBER_OF_CONTACTS_PER_PAGE), 1):
        table = PrettyTable()
        table.field_names = ["Contact Name", "Phone Number", 'Email',
                             "Birthday", "Days to Birthday"]

        for contact in contacts:
            contact_name = contact.user.name
            phone_numbers = [number.subrecord.phone for number in contact.phone_numbers]
            emails = [email.subrecord.email for email in contact.emails]
            birthday = contact.user.birthday_date if contact.user.birthday_date else '-'
            day_to_birthday = contact.days_to_birthday() if contact.user.birthday_date else '-'
            table.add_row(
                [contact_name.title(), phone_numbers, emails, birthday, day_to_birthday])
        print(f"{user_name}, this is page {i} of your phone book:\n{table}")
    return "End of contacts."


@input_error
def add_birthday_date(
        address_book: AB,
        user_name: str,
        contact_name: str,
        birthday_date) -> str:
    """Adds a birthday date to an existing contact in the phone book."""
    if contact_name and birthday_date:

        if contact_name not in address_book:
            raise KeyError(f"The contact '{contact_name.title()}' was not found.")

        contact = address_book.get_contact(contact_name)
        contact.add_birthday(birthday_date)
        address_book.add_record(contact)
    else:
        return "After the command, you must enter the existing contact's name and birthday in the format DD-MM-YYYY.\nFor example: 'Smith 23-04-1987'"

    return f"{user_name}, the birthday '{birthday_date}' has been added to the '{contact_name.title()}' contact."


@input_error
def change_birthday_date(
        address_book: AB,
        user_name: str,
        contact_name: str,
        new_birthday_date) -> str:
    """Changes the birthday date of an existing contact in the phone book."""
    if contact_name and new_birthday_date:

        if contact_name not in address_book:
            raise KeyError(f"The contact '{contact_name.title()}' was not found.")

        contact = address_book.get_contact(contact_name)
        contact.add_birthday(new_birthday_date)
        address_book.add_record(contact)
    else:
        return "After the command, you must enter the existing contact's name and new birthday in the format DD-MM-YYYY.\nFor example: 'Smith 23-04-1987'"

    return f"{user_name}, the birthday date for '{contact_name.title()}' has been changed to '{new_birthday_date}'."


@input_error
def serch_contact(address_book: AB, user_name: str, criteria: str):
    """Search for contacts in an address book based on a given criteria and print the results."""
   
    if criteria:

        if  not criteria.isdigit() and not criteria.isalpha():
            raise ValueError(f"Criteria '{criteria}' must be only numbers or letters")
         
        result = address_book.search(criteria)
        
        if isinstance(result, AB):
            print_all_contacts(result, user_name)
        else:
            return result
    else:
        return "After command, you must enter the criteria of serch"
    
    return f"{user_name}, {len(result)} contacts were found based on your search criteria!"


def close_bot(contact_name: str):
    """Close the bot"""
    sys.exit(f'{contact_name}, Good bye!')
