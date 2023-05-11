"""constants"""

from string import ascii_letters

FILE = 'address_book.bin'

NUMBER_OF_CONTACTS_PER_PAGE = 20

CYRILLIC = 'абвгґдеєёжзиіїйклмнопрстуфхцчшщъыьэюя. ʼ'
LETTERS = ascii_letters + CYRILLIC + CYRILLIC.upper()
NAME_RANGE = range(1, 50)
PHONE_RANGE = range(7, 20)

HELP = """
Description:\n
    This program is a console bot that recognizes commands entered from the keyboard and responds accordingly. 
It allows users to interact with the bot by entering commands and provides functionalities such as adding 
contacts, changing contacts, printing contact details.
"""
