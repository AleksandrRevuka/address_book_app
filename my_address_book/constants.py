"""
The constants module provides constant values used in the address book application.

This module defines various constant values used in the application, such as file paths,
number of contacts per page, and ranges for name and phone number lengths.
"""
import os
from string import ascii_letters
from string import punctuation

current_dir = os.getcwd()
FILE_AB = os.path.join(current_dir, "storage", "address_book.bin")
FILE_NB = os.path.join(current_dir, "storage", "notes_book.bin")


NUMBER_OF_CONTACTS_PER_PAGE = 20

CYRILLIC = "абвгґдеєёжзиіїйклмнопрстуфхцчшщъыьэюя. ʼ"
LETTERS = ascii_letters + CYRILLIC + CYRILLIC.upper()
PUNCTUATION = punctuation
NAME_RANGE = range(1, 50)
PHONE_RANGE = range(7, 20)
NOTE_LEN = 1
