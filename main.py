"""main"""

from address_book import AddressBook
from constants import COMMANDS, FILE
from utils import parse_args
from commands import (
    print_help,
    add_contact,
    print_contact,
    delete_contact,
    add_phone_number_to_contact,
    change_phone_number_contact,
    delete_phone_number_contact,
    add_email_to_contact,
    change_email_contact,
    delete_email_contact,
    add_birthday_to_contact,
    change_birthday_contact,
    serch_contact,
    print_contacts,
    close_bot,
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

            if command in ('--add_contact', '-ac'):
                message = add_contact(address_book,
                                      firstname,
                                      name,
                                      phone)

            elif command in ('--change_phone', '-cp'):
                message = change_phone_number_contact(address_book,
                                                    firstname,
                                                    name,
                                                    phone,
                                                    old_phone)

            elif command in ('--print_contact', '-pc'):
                message = print_contact(address_book, firstname, name)

            elif command in ('--del_contact', '-dc'):
                message = delete_contact(address_book, firstname, name)

            elif command in ('--del_phone', '-dp'):
                message = delete_phone_number_contact(address_book,
                                                    firstname,
                                                    name,
                                                    phone)

            elif command in ('--add_phone', '-ap'):
                message = add_phone_number_to_contact(address_book,
                                                      firstname,
                                                      name,
                                                      phone)

            elif command in ('--add_birth', '-ab'):
                birthday = phone
                message = add_birthday_to_contact(address_book,
                                                  firstname,
                                                  name,
                                                  birthday)

            elif command in ('--add_email', '-ae'):
                email = phone
                message = add_email_to_contact(address_book,
                                               firstname,
                                               name,
                                               email)
                
            elif command in ('--change_email', '-ce'):
                new_email = phone
                old_email = old_phone
                message = change_email_contact(address_book,
                                               firstname,
                                               name,
                                               new_email,
                                               old_email)
                
            elif command in ('--del_email', '-de'):
                email = phone
                message = delete_email_contact(address_book,
                                               firstname,
                                               name,
                                               email)

            elif command in ('--change_birth', '-cb'):
                birthday = phone
                message = change_birthday_contact(address_book,
                                                firstname,
                                                name,
                                                birthday)

            elif command in ('--show_contacts', '-s'):
                message = print_contacts(address_book, firstname)

            elif command in ('--serch', '-sc'):
                criteria = name
                message = serch_contact(address_book, firstname, criteria)

            elif command in ('--quit', '-q'):
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
