"""main"""

from address_book import AddressBook
from constants import COMMANDS, FILE
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
    serch_contact,
    print_all_contacts,
    close_bot,
    print_help,
)


def say_hello_to_anyone(firstname: str, lastname: str) -> str:
    """Say hello to anyone"""
    if lastname:
        hello_message = f'Hello, {firstname} {lastname}! How can I assist you today?'
    else:
        hello_message = f'Hello, {firstname}! How can I assist you today?'
    return hello_message


def run_bot():
    """Main controller"""
    cli_args = parse_args()
    firstname = cli_args.first.lower().title()
    lastname = cli_args.last.lower().title()

    print(say_hello_to_anyone(firstname, lastname))

    address_book = AddressBook()
    address_book.read_records_from_file(FILE)

    while True:
        usedr_data = input('Enter a command: ').lower()
        data = usedr_data.split()

        if not data:
            continue

        command = data[0]
        name = data[1] if len(data) > 1 else None
        phone = data[2] if len(data) > 2 else None
        old_phone = data[3] if len(data) > 3 else None

        if command in COMMANDS:

            if command in ('--add', '-a'):
                message = add_contact(address_book,
                                      firstname,
                                      name,
                                      phone)

            elif command in ('--change', '-c'):
                message = change_number_contact(address_book,
                                                firstname,
                                                name,
                                                phone,
                                                old_phone)

            elif command in ('--print', '-p'):
                message = print_contact(address_book, firstname, name)

            elif command in ('--del'):
                message = delete_contact(address_book, firstname, name)

            elif command in ('--del_phone'):
                message = delete_contact_phone(address_book,
                                               firstname,
                                               name,
                                               phone)

            elif command in ('--add_phone'):
                message = add_number_phone_to_contact(address_book,
                                                      firstname,
                                                      name,
                                                      phone)

            elif command in ('--add_birth'):
                birthday = phone
                message = add_birthday_date(address_book,
                                            firstname,
                                            name,
                                            birthday)

            elif command in ('--change_birth'):
                birthday = phone
                message = change_birthday_date(address_book,
                                               firstname,
                                               name,
                                               birthday)

            elif command in ('--show_all', '-s'):
                message = print_all_contacts(address_book, firstname)

            elif command in ('--serch'):
                criteria = name
                message = serch_contact(address_book, firstname, criteria)

            elif command in ('--goodbye', '--close', '--exit', '-q'):
                address_book.save_records_to_file(FILE)
                close_bot(firstname)

            elif command in ('--help', '-h'):
                message = print_help(firstname)

            print(message)

        else:
            print(
                f"Unrecognized command: '{command}'.\nPlease refer to the help (-h or --help) for a list of available commands.")


if __name__ == '__main__':
    run_bot()
