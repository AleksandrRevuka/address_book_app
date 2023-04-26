"""main"""

from constants import COMMANDS
from utils import parse_args
from commands import (
    add_contact,
    change_number_contact,
    print_contact,
    delete_contact,
    delete_contact_phone,
    add_number_phone_to_contact,
    add_birthday_date,
    change_birthday_date,
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
        usedr_data = input('Enter a command: ').lower()
        data = usedr_data.split()
        command = data[0]
        name = data[1] if len(data) > 1 else False
        phone = data[2] if len(data) > 2 else False
        old_phone = data[3] if len(data) > 3 else False

        if command in COMMANDS:

            if command in ('--add', '-a'):
                if name and phone:
                    message = add_contact(firstname, name, phone)
                else:
                    print(
                        f"After the '{command}' command, you must enter the new contact's name and phone number separated by a space.\nFor example: '{command} Smith 380631234567'")

            elif command in ('--change', '-c'):
                if name and phone and old_phone:
                    message = change_number_contact(
                        firstname,
                        name,
                        phone,
                        old_phone)
                else:
                    print(
                        f"After the '{command}' command, you must enter the existing contact's name, the new phone number, and the old phone number, separated by spaces.\nFor example: '{command} Smith 380631234567 +380956785434'")

            elif command in ('--print', '-p'):
                if name:
                    message = print_contact(firstname, name)
                else:
                    print(
                        f"After the '{command}' command, you must enter the existing contact's name.\nFor example: '{command} Smith'")

            elif command in ('--del'):
                if name:
                    message = delete_contact(firstname, name)
                else:
                    print(
                        f"After the '{command}' command, you must enter the existing contact's name.\nFor example: '{command} Smith'")

            elif command in ('--del_phone'):
                if name:
                    message = delete_contact_phone(firstname, name, phone)
                else:
                    print(
                        f"After the '{command}' command, you must enter the existing contact's name and phone number separated by a space.\nFor example: '{command} Smith 380631234567'")

            elif command in ('--add_phone'):
                if name and phone:
                    message = add_number_phone_to_contact(firstname, name, phone)
                else:
                    print(
                        f"After the '{command}' command, you must enter the existing contact's name and new phone number separated by a space.\nFor example: '{command} Smith 380631234567'")

            elif command in ('--add_birth'):
                birthday = phone
                if name and birthday:
                    message = add_birthday_date(firstname, name, birthday)
                else:
                    print(
                        f"After the '{command}' command, you must enter the existing contact's name and birthday in the format DD-MM-YYYY.\nFor example: '{command} Smith 23-04-1987'")

            elif command in ('--change_birth'):
                birthday = phone
                if name and birthday:
                    message = change_birthday_date(firstname, name, birthday)
                else:
                    print(
                        f"After the '{command}' command, you must enter the existing contact's name and new birthday in the format DD-MM-YYYY.\nFor example: '{command} Smith 23-04-1987'")

            elif command in ('--show_all', '-s'):
                message = print_all_contacts(firstname)

            elif command in ('--goodbye', '--close', '--exit', '-q'):
                close_bot(firstname)

            elif command in ('--help', '-h'):
                message = print_help(firstname)

            else:
                message = help_from_bot(firstname)

            print(message)

        else:
            print(
                f"Unrecognized command: '{command}'.\nPlease refer to the help (-h or --help) for a list of available commands.")


if __name__ == '__main__':
    run_bot()
