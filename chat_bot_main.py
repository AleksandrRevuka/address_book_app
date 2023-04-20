"""
A console bot helper that will recognize commands entered from the keyboard and respond accordingly
"""

import sys
import argparse
from string import ascii_letters, digits
from collections import UserDict

from prettytable import PrettyTable


CYRILLIC = 'абвгґдеєёжзиіїйклмнопрстуфхцчшщъыьэюя'
LETTERS = ascii_letters + CYRILLIC + CYRILLIC.upper()
PHONE_RANGE = range(11, 17)

COMMANDS = {
    "--help": 'print_help',
    "-h": 'print_help',
    "--hello": 'help_from_bot',
    "--add": 'add_contact',
    "-a": 'add_contact',
    "--change": 'change_number_contact',
    "-c": 'change_number_contact',
    "--phone": 'print_number_contact',
    "-p": 'print_number_contact',
    "--del": 'delete_contact',
    "--del_phone": 'delete_contact_phone',
    "--add_phone": 'add_number_phone_to_contact',
    "--show_all": 'print_all_contacts',
    "-s": 'print_all_contacts',
    "--goodbye": 'close_bot',
    "--close": 'close_bot',
    "--exit": 'close_bot',
    "-q": 'close_bot',
}

HELP = """
Description:
    This program is a console bot that recognizes commands entered from the keyboard and responds accordingly. 
    It allows users to interact with the bot by entering commands and provides functionalities such as adding 
    contacts, changing contacts, printing contact details, and closing the bot.

Usage:
    chat_bot_main.py --first <firstname> [--last <lastname>]
    chat_bot_main.py -f <firstname> [-l <lastname>]

Commands:
    --hello         : Provide help from the bot.
    -h, --help      : Show this help message.
    -a, --add       : Add a contact to the phone book.
    -c, --change    : Change a contact in the phone book.
    -p, --phone     : Get the phone number of a contact.
    --del           : Remove a contact from the phone book.
    --del_phone     : Remove a phone number from a contact in the phone book.
    --add_phone     : Add a new phone number to an existing contact in the phone book.
    -s, --show_all  : Show all contacts in the phone book.
    --goodbye       : Close the bot.
    --close         : Close the bot.
    --exit          : Close the bot.
    -q              : Close the bot.

Options:
    -f, --first     : First name of the user (required).
    -l, --last      : Last name of the user (optional).

Note: Names and phone numbers should only contain letters and digits.
"""


class AddressBook(UserDict):
    """ A class that represents an address book containing contact records."""

    def get_contact(self, name):
        """Returns the contact record for the given name."""
        return self.data[name]
    
    def add_record(self, record):
        """Adds a new contact record to the address book."""
        self.data[record.name.value] = record
    
    def delete_record(self, record_name):
        """Removes a contact record from the address book."""
        del self.data[record_name]
    
    def search(self):
        """Searches the address book for contacts matching the given criteria."""
        pass


class Record:
    """ A class that represents a contact record in a phone book."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Adds a new phone number to the contact."""
        self.phones.append(Phone(phone))
    
    def edit_phone(self, phone_number, new_phone_number):
        """Updates an existing phone number for the contact."""
        for phone in self.phones:
            if phone.value == phone_number:
                phone.value = new_phone_number
                break
    
    def delete_phone(self, phone_number):
        """Removes a phone number from the contact."""
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

class Field:
    """..."""
    def __init__(self, value):
        self.value = value


class Name(Field):
    """..."""
    pass


class Phone(Field):
    """..."""
    pass


def parse_args() -> argparse.Namespace:
    """Parse args with argparse"""
    parser = argparse.ArgumentParser(
        prog='Chat bot',
        usage='%(prog)s chat_bot_main.py --first <firstname> [--last <lastname>]',
        description='This program is a console bot that recognizes commands entered from the keyboard and \
        responds accordingly. It allows users to interact with the bot by entering commands and provides \
        functionalities such as adding contacts, changing contacts, printing contact details, and closing \
        the bot.'
    )
    parser.add_argument(
        '-f',
        '--first',
        type=str,
        help='enter your firstname',
        required=True,
    )
    parser.add_argument(
        '-l',
        '--last',
        type=str,
        help='enter your lastname',
        default='',
        required=False,
    )

    args = parser.parse_args()
    return args


def say_hello_to_anyone(firstname: str, lastname: str) -> str:
    """Say hello to anyone"""
    if lastname:
        hello_message = f'Hello, {firstname} {lastname}!'
    else:
        hello_message = f'Hello, {firstname}!'
    return hello_message


def input_error(func):
    """Decorator for handling input errors"""
    def wrraper_input_error(*args, **kwargs):
        """Wrapper function for handling input errors"""
        try:
            return func(*args, **kwargs)

        except TypeError as error:
            return f"Error: {error}"

        except ValueError as error:
            return f"Error: {error}"

        except KeyError as error:
            return f"Error: {error}"

    return wrraper_input_error


def print_help(your_name: str):
    """Print help for the console bot program."""
    return f'{your_name}, This is help for the console bot program:\n{HELP}'


def help_from_bot(your_name) -> str:
    """Provide help from the bot."""
    return f'{your_name}, How can I help you?'


@input_error
def add_contact(your_name: str, name: str, phone: str) -> dict:
    """Add a contact to the phone book."""

    if len(name.strip(LETTERS)) != 0:
        raise TypeError(f"Contact's name '{name.title()}' can only contain letter")
    
    if name in phone_book:
        raise ValueError(f"Contact '{name.title()}' exists in the address book")

    if len(phone.strip(digits + '+')) != 0:
        raise TypeError(f"Contact's phone '{phone}' can only contain digits")

    if len(phone) not in PHONE_RANGE:
        raise ValueError(
            f"Contact's phone '{phone}' is too long or short, it must be between 11 and 16 numbers")
    

    contact = Record(name)
    contact.add_phone(phone)
    phone_book.add_record(contact)

    return f"{your_name}, contact has been added '{name.title()}': {phone}"

 
@input_error
def change_number_contact(your_name: str, name: str, phone: str, old_phone: str):
    """Change the phone number of a contact in the phone book."""

    for number in phone, old_phone:
        if len(number.strip(digits + '+')) != 0:
            raise TypeError(f"Contact's phone '{number}' can only contain digits")

        if len(number) not in PHONE_RANGE:
            raise ValueError(
                f"Contact's phone '{number}' is too long or short, it must be between 11 and 16 numbers")

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
    """Prints the phone number of a contact from the phone book."""

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

    if len(phone.strip(digits + '+')) != 0:
        raise TypeError("Contact's phone '{phone}' can only contain digits")

    if len(phone) not in PHONE_RANGE:
        raise ValueError(
            f"Contact's phone '{phone}' is too long or short, it must be between 11 and 16 numbers")

    contact = phone_book.get_contact(name)
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


def close_bot(name):
    """Close the bot"""
    sys.exit(f'{name} Good bye!')


def format_phone_number(func):
    """Add '+' to phone's number"""
    def add_code_phone(phone):
        phone = func(phone)
        return ''.join('+' + phone)

    return add_code_phone


@format_phone_number
def sanitize_phone_number(phone: str):
    """Clean number"""
    return ''.join(number.strip(' , (, ), -, +') for number in phone)


def main():
    """Main controller"""
    cli_args = parse_args()
    firstname = cli_args.first.lower().title()
    lastname = cli_args.last.lower().title()

    print(say_hello_to_anyone(firstname, lastname))

    while True:
        usedr_data = input('Enter command: ').lower()
        data = usedr_data.split()
        command = data[0]
        name = data[1] if len(data) > 1 else False
        phone = data[2] if len(data) > 2 else False
        old_phone = data[3] if len(data) > 3 else False

        if command in COMMANDS:

            if command in ('--add', '-a'):
                if name and phone:
                    phone = sanitize_phone_number(phone)
                    print(add_contact(firstname, name, phone))
                else:
                    print(f"After the command {command} you must enter the new contact's name and new number with a space\nFor example: {command} Smith 380631234567")

            elif command in ('--change', '-c'):
                if name and phone and old_phone:
                    phone = sanitize_phone_number(phone)
                    old_phone = sanitize_phone_number(old_phone)
                    print(change_number_contact(firstname, name, phone, old_phone))
                else:
                    print(f"After the command {command} you must enter existing name and new contact number and old contact number separated by a space\nFor example: {command} Smith 380631234567 +380956785434")

            elif command in ('--phone', '-p'):
                if name:
                    print(print_number_contact(firstname, name))
                else:
                    print(f"After the command {command} you must enter the existing contact's name\nFor example: {command} Smith")

            elif command in ('--del'):
                if name:
                    print(delete_contact(firstname, name))
                else:
                    print(f"After the command {command} you must enter the existing contact's name\nFor example: {command} Smith")
            
            elif command in ('--del_phone'):
                if name:
                    phone = sanitize_phone_number(phone)
                    print(delete_contact_phone(firstname, name, phone))
                else:
                    print(f"After the command {command} you must enter the existing contact's name and phone\nFor example: {command} Smith 380631234567")

            elif command in ('--add_phone'):
                if name and phone:
                    phone = sanitize_phone_number(phone)
                    print(add_number_phone_to_contact(firstname, name, phone))
                else:
                    print(f"After the command {command} you must enter the existing contact's name and new number with a space\nFor example: {command} Smith 380631234567")

            elif command in ('--show_all', '-s'):
                print(print_all_contacts(firstname))

            elif command in ('--goodbye', '--close', '--exit', '-q'):
                print(close_bot(firstname))

            elif command in ('--help', '-h'):
                print(print_help(firstname))

            else:
                print(help_from_bot(firstname))

        else:
            print(f"I don't know this command: {command}\nYou can see halp (-h or --help)!\nTry again!")

phone_book = AddressBook()

if __name__ == '__main__':
    main()

# python chat_bot_main.py -f sasha
# -a Olya 380956786543
# -c olya 380955436712 380956786543
# --add_phone olya 380956786543

# --add Alex 380964563456
# -c alex 380964563499 380964563456
# --add_phone alex 380675876987
# --add_phone alex 380964563456
# --del olya
# --del_phone alex 380964563499