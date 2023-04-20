"""utils"""

import argparse


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


def format_phone_number(func):
    """Add '+' to phone's number"""
    def add_code_phone(phone):
        phone = func(phone)
        return ''.join('+' + phone)

    return add_code_phone


@format_phone_number
def sanitize_phone_number(phone: str) -> str:
    """Clean number"""
    return ''.join(number.strip(' , (, ), -, +') for number in phone)
