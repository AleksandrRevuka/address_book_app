"""main"""

from constants import COMMANDS
from utils import sanitize_phone_number, parse_args
from commands import (
    add_contact,
    change_number_contact,
    print_number_contact,
    delete_contact,
    delete_contact_phone,
    add_number_phone_to_contact,
    print_all_contacts,
    help_from_bot,
    close_bot,
    print_help,
)


def say_hello_to_anyone(firstname: str, lastname: str) -> str:
    """Say hello to anyone"""
    if lastname:
        hello_message = f'Hello, {firstname} {lastname}!'
    else:
        hello_message = f'Hello, {firstname}!'
    return hello_message


def run_bot():
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
                    print(
                        f"After the command {command} you must enter the new contact's name and new number with a space\nFor example: {command} Smith 380631234567")

            elif command in ('--change', '-c'):
                if name and phone and old_phone:
                    phone = sanitize_phone_number(phone)
                    old_phone = sanitize_phone_number(old_phone)
                    print(change_number_contact(
                        firstname, name, phone, old_phone))
                else:
                    print(
                        f"After the command {command} you must enter existing name and new contact number and old contact number separated by a space\nFor example: {command} Smith 380631234567 +380956785434")

            elif command in ('--phone', '-p'):
                if name:
                    print(print_number_contact(firstname, name))
                else:
                    print(
                        f"After the command {command} you must enter the existing contact's name\nFor example: {command} Smith")

            elif command in ('--del'):
                if name:
                    print(delete_contact(firstname, name))
                else:
                    print(
                        f"After the command {command} you must enter the existing contact's name\nFor example: {command} Smith")

            elif command in ('--del_phone'):
                if name:
                    phone = sanitize_phone_number(phone)
                    print(delete_contact_phone(firstname, name, phone))
                else:
                    print(
                        f"After the command {command} you must enter the existing contact's name and phone\nFor example: {command} Smith 380631234567")

            elif command in ('--add_phone'):
                if name and phone:
                    phone = sanitize_phone_number(phone)
                    print(add_number_phone_to_contact(firstname, name, phone))
                else:
                    print(
                        f"After the command {command} you must enter the existing contact's name and new number with a space\nFor example: {command} Smith 380631234567")

            elif command in ('--show_all', '-s'):
                print(print_all_contacts(firstname))

            elif command in ('--goodbye', '--close', '--exit', '-q'):
                print(close_bot(firstname))

            elif command in ('--help', '-h'):
                print(print_help(firstname))

            else:
                print(help_from_bot(firstname))

        else:
            print(
                f"I don't know this command: {command}\nYou can see halp (-h or --help)!\nTry again!")


if __name__ == '__main__':
    run_bot()
