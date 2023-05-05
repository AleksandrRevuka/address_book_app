"""constants"""

FILE = 'address_book.bin'

NUMBER_OF_CONTACTS_PER_PAGE = 5

COMMANDS = {
    "--help": 'print_help',
    "-h": 'print_help',
    
    "--add_contact": 'add_contact',
    "-ac": 'add_contact',
    "--print_contact": 'print_contact',
    "-pc": 'print_contact',
    "--del_contact": 'delete_contact',
    "-dc": 'delete_contact',
    
    "--add_phone": 'add_phone_number_to_contact',
    "-ap": 'add_phone_number_to_contact',
    "--change_phone": 'change_phone_number_contact',
    "-cp": 'change_phone_number_contact',
    "--del_phone": 'delete_phone_number_contact',
    "-dp": 'delete_phone_number_contact',
    
    "--add_email": 'add_email_to_contact',
    "-ae": 'add_email_to_contact',
    "--change_email": 'change_email_contact',
    "-ce": 'change_email_contact',
    "--del_email": 'delete_email_contact',
    "-de": 'delete_email_contact',
    
    "--add_birth": 'add_birthday_to_contact',
    "-ab": 'add_birthday_to_contact',
    "--change_birth": 'change_birthday_contact',
    "-cb": 'change_birthday_contact',
    
    "--serch": 'serch_contact',
    "-sc": 'serch_contact',
    
    "--show_contacts": 'print_contacts',
    "-s": 'print_contacts',
    
    "--quit": 'close_bot',
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
    -p, --print     : Get the phone number of a contact.
    --del           : Remove a contact from the phone book.
    --del_phone     : Remove a phone number from a contact in the phone book.
    --add_phone     : Add a new phone number to an existing contact in the phone book.
    --add_birth"    : Add birthday date.
    --change_birth" : Change birthday date.
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
