"""constants"""

NUMBER_OF_CONTACTS_PER_PAGE = 2

COMMANDS = {
    "--help": 'print_help',
    "-h": 'print_help',
    "--hello": 'help_from_bot',
    "--add": 'add_contact',
    "-a": 'add_contact',
    "--change": 'change_number_contact',
    "-c": 'change_number_contact',
    "--print": 'print_contact',
    "-p": 'print_number_contact',
    "--del": 'delete_contact',
    "--del_phone": 'delete_contact_phone',
    "--add_phone": 'add_number_phone_to_contact',
    "--add_birth": 'add_birthday_date',
    "--change_birth": 'change_birthday_date',
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
