"""constants"""
import os
from string import ascii_letters

current_dir = os.getcwd()
FILE = os.path.join(current_dir, 'address_book.bin')


NUMBER_OF_CONTACTS_PER_PAGE = 20

CYRILLIC = 'абвгґдеєёжзиіїйклмнопрстуфхцчшщъыьэюя. ʼ'
LETTERS = ascii_letters + CYRILLIC + CYRILLIC.upper()
NAME_RANGE = range(1, 50)
PHONE_RANGE = range(7, 20)
