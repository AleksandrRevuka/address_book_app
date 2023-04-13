"""
A console bot helper that will recognize commands entered from the keyboard and respond accordingly
"""

import sys
import argparse
from prettytable import PrettyTable


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


phone_book = {}


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
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Incorrect input. Please try again."

    return wrraper_input_error


def print_help(your_name: str):
    """..."""
    return f'{your_name}, This is help for the console bot program:\n{HELP}'


def help_from_bot(name) -> str:
    """..."""
    return f'{name}, How can I help you?'


def add_contact(your_name: str, name: str, phone: str) -> dict:
    """..."""
    phone_book.update({name: phone})
    return f'{your_name}, contact has been added {name}: {phone}'


def change_contact(your_name: str, name: str, phone: str):
    """..."""
    # if not name.isalpha():
    #     raise ValueError("The name can only contain letters")

    phone_book[name] = phone
    return f'{your_name}, contact has been changed {name}: {phone}'


def print_number_contact(your_name: str, name: str) -> str:
    """..."""
    return f"{your_name}, This contact {name} has phone number: {phone_book[name]} "


def print_all_contacts(your_name: str) -> str:
    """..."""
    table = PrettyTable()
    table.field_names = ["Name contact", "number phone"]

    for name, phone in phone_book.items():
        table.add_row([name, phone])

    return f"{your_name}, This is your phone book:\n{table}"


def close_bot(name):
    """..."""
    sys.exit(f'{name} Good bye!')


COMANDS = {
    "--help": print_help,
    "-h": print_help,
    "--hello": help_from_bot,
    "--add": add_contact,
    "-a": add_contact,
    "--change": change_contact,
    "-c": change_contact,
    "--phone": print_number_contact,
    "-p": print_number_contact,
    "--show all": print_all_contacts,
    "-s": print_all_contacts,
    "--good bye": close_bot,
    "--close": close_bot,
    "--exit": close_bot,
    "-q": close_bot,

}


@input_error
def handle_command(command, name=None, phone=None):
    """..."""
    return COMANDS[command]


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
        name = data[1].title() if len(data) > 1 else None
        phone = ''.join(data[2:]).title() if len(data) > 2 else None

        if command in COMANDS:
            if command in ('--add', '-a'):
                response = handle_command(command)
                print(response(firstname, name, phone))
            elif command in ('--change', '-c'):
                response = handle_command(command, name, phone)
                print(response(firstname, name, phone))
            elif command in ('--phone', '-p'):
                response = handle_command(command)
                print(response(firstname, name))
            else:
                response = handle_command(command)
                print(response(firstname))
        else:
            print(
                f"I don't know this command: {command}\nYou can see halp (-h or --help)!\nTry again!")


if __name__ == '__main__':
    main()
