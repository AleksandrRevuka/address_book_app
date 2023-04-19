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

HELP = """
A console bot helper that will recognize commands entered from the keyboard and respond accordingly

Usage:
    chat_bot_main.py --first <firstname> [--last <lastname>]
    chat_bot_main.py -f <firstname> [-l <lastname>]

Commands:
    --hello         : Get a greeting from the bot.
    -h              : Get a greeting from the bot.
    --add           : Add a contact to the phone book.
    -a              : Add a contact to the phone book.
    --change        : Change a contact in the phone book.
    -c              : Change a contact in the phone book.
    --phone         : Get the phone number of a contact.
    -p              : Get the phone number of a contact.
    --show all      : Show all contacts in the phone book.
    -s              : Show all contacts in the phone book.
    --good bye      : Close the bot.
    --close         : Close the bot.
    --exit          : Close the bot.
    -q              : Close the bot.

Options:
    -f, --first     : First name of the user (required).
    -l, --last      : Last name of the user (optional).

Note: Names and phone numbers should only contain letters and digits.
"""


class AddressBook(UserDict):
    """..."""

    def get_contact(self, name):
        """..."""
        return self.data[name]
    
    def add_record(self, record):
        """..."""
        self.data[record.name.value] = record
    
    def delete_record(self, record_name):
        """..."""
        del self.data[record_name]
    
    def search(self):
        """..."""
        pass


class Record:
    """..."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """..."""
        self.phones.append(Phone(phone))
    
    def edit_phone(self, phone_number, new_phone_number):
        """..."""
        for phone in self.phones:
            if phone.value == phone_number:
                phone.value = new_phone_number
                break
    
    def delete_phone(self, phone_number):
        """..."""
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
        raise TypeError("Contact's name can only contain letter")

    if len(phone.strip(digits + '+')) != 0:
        raise TypeError("Contact's phone can only contain digits")

    if len(phone) not in PHONE_RANGE:
        raise ValueError(
            f"Contact's phone {phone} is too long or short, it must be between 11 and 16 numbers")

    contact = Record(name)
    contact.add_phone(phone)
    phone_book.add_record(contact)

    return f'{your_name}, contact has been added {name.title()}: {phone}'

 
@input_error
def change_number_contact(your_name: str, name: str, phone: str, old_phone: str):
    """Change the phone number of a contact in the phone book."""

    if len(phone.strip(digits + '+')) != 0:
        raise TypeError("Contact's phone can only contain digits")

    if len(phone) not in PHONE_RANGE:
        raise ValueError(
            f"Contact's phone {phone} is too long or short, it must be between 11 and 16 numbers")

    if name not in phone_book:
        raise KeyError(f"Contact {name.title()} not found")

    contact = phone_book.get_contact(name)
    contact.edit_phone(old_phone, phone)
    phone_book.add_record(contact)

    return f'{your_name}, contact has been changed {name.title()}: {phone}'


@input_error
def print_number_contact(your_name: str, name: str) -> str:
    """Print the phone number of a contact from the phone book."""

    if name not in phone_book:
        raise KeyError(f"Contact {name} not found")
    
    contact = phone_book.get_contact(name)
    contact_numbers = [number.value for number in contact.phones]

    return f"{your_name}, This contact {name.title()} has phone number: {contact_numbers} "


@input_error
def delete_contact(your_name: str, name: str) -> str:
    """..."""

    if name not in phone_book:
        raise KeyError(f"Contact {name} not found")
    
    phone_book.delete_record(name)

    return f"{your_name}, This contact {name.title()} has been deleted"


@input_error
def delete_contact_phone(your_name: str, name: str, phone: str) -> str:
    """..."""

    if name not in phone_book:
        raise KeyError(f"Contact {name} not found")
    
    contact = phone_book.get_contact(name)

    if phone in contact.phones:
        raise ValueError(f"Contact's phone {phone} not found in the address book")

    contact.delete_phone(phone)

    return f"{your_name}, Contact's phone {phone} was deleted from the address book"


@input_error
def add_number_phone_to_contact(your_name: str, name: str, phone: str) -> str:
    """..."""
    if name not in phone_book:
        raise KeyError(f"Contact {name} not found")

    if len(phone.strip(digits + '+')) != 0:
        raise TypeError("Contact's phone can only contain digits")

    if len(phone) not in PHONE_RANGE:
        raise ValueError(
            f"Contact's phone {phone} is too long or short, it must be between 11 and 16 numbers")

    contact = phone_book.get_contact(name)
    contact.add_phone(phone)

    return f"{your_name}, {name}'s new contact phone {phone} has been successfully added to the address book"


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


COMMANDS = {
    "--help": print_help,
    "-h": print_help,
    "--hello": help_from_bot,
    "--add": None,
    "-a": None,
    "--change": None,
    "-c": None,
    "--phone": None,
    "-p": None,
    "--del": None,
    "--del_phone": None,
    "--add_phone": None,
    "--show_all": print_all_contacts,
    "-s": print_all_contacts,
    "--goodbye": close_bot,
    "--close": close_bot,
    "--exit": close_bot,
    "-q": close_bot,

}


def handle_command(command):
    """This function returns the appropriate function to handle the given command."""
    return COMMANDS[command]


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

    hello_message = say_hello_to_anyone(firstname, lastname)
    print(hello_message)

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
                    # phone = sanitize_phone_number(phone)
                    print(add_contact(firstname, name, phone))
                else:
                    print(f"After the command {command} you must enter the new contact's name and new number with a space\nFor example: {command} Smith 380631234567")

            elif command in ('--change', '-c'):
                if name and phone and old_phone:
                    # phone = sanitize_phone_number(phone)
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
                    print(delete_contact_phone(firstname, name, phone))
                else:
                    print(f"After the command {command} you must enter the existing contact's name and phone\nFor example: {command} Smith 380631234567")
            elif command in ('--add_phone'):
                if name and phone:
                    # phone = sanitize_phone_number(phone)
                    print(add_number_phone_to_contact(firstname, name, phone))
                else:
                    print(f"After the command {command} you must enter the existing contact's name and new number with a space\nFor example: {command} Smith 380631234567")

            else:
                response = handle_command(command)
                print(response(firstname))
        else:
            print(f"I don't know this command: {command}\nYou can see halp (-h or --help)!\nTry again!")

phone_book = AddressBook()

if __name__ == '__main__':
    main()

# python chat_bot_main.py -f sasha
# -a Olya 380956786543
# --add Alex 380964563456
# -c alex 380964563499 380964563456 
# --del olya
# --del_phone alex 380964563499