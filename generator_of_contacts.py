"""..."""
from datetime import datetime
import random
from faker import Factory


from my_address_book.address_book import Record, AddressBook as AB
from my_address_book.entities import Phone, User, Email
from my_address_book.constants import FILE
from my_address_book.utils import sanitize_phone_number


def generator_contacts(n=10) -> list[dict]:
    """
    The generator_contacts function generates a list of contacts.
    """
    locales = ['en_US'] #'uk_UA'
    locale = random.choice(locales)
    contacts = []
    for _ in range(n):
        fake = Factory.create(locale)
        contact = {}
        contact['name'] = fake.first_name()
        contact['birthday'] = fake.date()
        contact['phone_number'] = fake.phone_number()
        contact['email'] = fake.ascii_email()
        print(contact)
        contacts.append(contact)
    return contacts


def move_to_address_book(contacts, address_book):
    """
    The move_to_address_book function takes a list of dictionaries and an address book as arguments.
    It then iterates through the list of dictionaries, creating a Record object for each dictionary in the list.
    The function then adds that record to the address book.
    """
    for contact in contacts:
        contact_name = contact['name'].strip()
        birthday = datetime.strptime(contact['birthday'], '%Y-%m-%d')
        # birthday = date_object.strftime('%d-%m-%Y')
        phone = sanitize_phone_number(contact['phone_number'])
        phone = Phone(phone)
        email = Email(contact['email'])
        user = User(contact_name)
        contact = Record(user)
        contact.add_email(email)
        contact.add_phone_number(phone)
        contact.add_birthday(birthday.date())
        address_book.add_record(contact)
    return address_book


if __name__ == '__main__':
    address_book = AB()
    contacts = generator_contacts(120)
    address_book = move_to_address_book(contacts, address_book)
    address_book.save_records_to_file(FILE)
