"""commands"""

import click
from prettytable import PrettyTable

from utils import sanitize_phone_number
from validation import (
    name_validation,
    phone_validation,
    email_validation,
    birthday_date_validation,
    criteria_validation,
    check_name_in_address_book,
    check_name_not_in_address_book,
    check_phone_number_in_address_book,
    check_phone_number_not_in_address_book,
    check_email_in_address_book,
    check_email_not_in_address_book,
)
from constants import (NUMBER_OF_CONTACTS_PER_PAGE, FILE)
from address_book import Record, AddressBook as AB
from entities import Phone, User, Email


def add_contact(addressbook: AB,
                contact_name: str,
                phone_number: str) -> None:
    """
    Adds a contact to the phone book.
    
    :param addressbook: AB: Pass the addressbook object to the function\n
    :param contact_name: str: Pass the name of the contact to be added\n
    :param phone_number: str: Verify the phone number
    """
    check_name_in_address_book(addressbook, contact_name)
    name_validation(contact_name)
    phone_number = sanitize_phone_number(phone_number)
    phone_validation(phone_number)

    phone = Phone(phone_number)
    user = User(contact_name)
    contact = Record(user)
    contact.add_phone_number(phone)
    addressbook.add_record(contact)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The contact '{contact_name.title()}' has been added: {phone.phone}", fg='blue')


def print_contact(addressbook: AB, contact_name: str) -> None:
    """
    The print_contact function prints the phone number and other details of a contact from the addressbook.
    
    :param addressbook: AB: Pass the addressbook object to the function\n
    :param contact_name: str: Specify the name of the contact to be printed\n
    """
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    table = PrettyTable()
    table.field_names = ["Contact name", "Phone number",
                         "Email", "Birthday", "Days to Birthday"]

    contact = addressbook.get_contact(contact_name)
    phone_numbers = [number.subrecord.phone for number in contact.phone_numbers]
    emails = [email.subrecord.email for email in contact.emails]
    birthday = contact.user.birthday_date.strftime('%d-%m-%Y') if contact.user.birthday_date else '-'
    day_to_birthday = contact.days_to_birthday() if contact.user.birthday_date else '-'
    table.add_row([contact_name.title(), phone_numbers, emails, birthday, day_to_birthday])

    click.secho(f"\n{table}\n", fg='blue')


def delete_contact(addressbook: AB, contact_name: str) -> None:
    """
    The delete_contact function deletes a contact from the addressbook.
    
    :param addressbook: AB: Pass the addressbook object to the function\n
    :param contact_name: str: Pass in the name of the contact to be deleted
    """
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    addressbook.delete_record(contact_name)
    addressbook.save_records_to_file(FILE)
    click.secho(f"The contact '{contact_name.title()}' has been deleted.", fg='blue')


def add_phone_number_to_contact(addressbook: AB, contact_name: str, phone_number: str) -> None:
    """
    The add_phone_number_to_contact function adds a phone number to an existing contact.
    
    :param addressbook: AB: Pass the addressbook object to the function\n
    :param contact_name: str: Get the name of the contact that we want to add a phone number to\n
    :param phone_number: str: Pass the phone number to be added to the contact
    """
    contact_name = contact_name.lower()
    phone_number = sanitize_phone_number(phone_number)
    phone_validation(phone_number)
    phone = Phone(phone_number)

    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    check_phone_number_in_address_book(contact, phone, contact_name)

    contact.add_phone_number(phone)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The phone number '{phone.phone}' has been successfully added to the '{contact_name.title()}' contact.", fg='blue')


def change_phone_number_contact(addressbook: AB,
                                contact_name: str,
                                new_phone_number: str,
                                old_phone_number: str) -> None:
    """
    The change_phone_number_contact function is used to change the phone number of a contact in the address book.
        The function takes in an AddressBook object, a string representing the name of the contact whose phone number will be changed,
        and two strings representing both old and new phone numbers.
    
    :param addressbook: AB: Pass the addressbook object to the function\n
    :param contact_name: str: Specify the name of the contact that we want to change\n
    :param new_phone_number: str: Store the new phone number that will be used to replace the old one\n
    :param old_phone_number: str: Verify that the phone number exists in the contact's list of phone numbers
    """
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)
    contact = addressbook.get_contact(contact_name)

    old_phone_number = sanitize_phone_number(old_phone_number)
    phone_validation(old_phone_number)
    old_phone = Phone(old_phone_number)
    check_phone_number_not_in_address_book(contact, old_phone, contact_name)

    new_phone_number = sanitize_phone_number(new_phone_number)
    phone_validation(new_phone_number)
    new_phone = Phone(new_phone_number)
    check_phone_number_in_address_book(contact, new_phone, contact_name)

    contact.change_phone_number(old_phone, new_phone)
    addressbook.add_record(contact)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The contact '{contact_name.title()}' has been updated with the new phone number: {new_phone.phone}", fg='blue')


def delete_phone_number_contact(addressbook: AB,
                                contact_name: str,
                                phone_number: str) -> None:
    """
    The delete_phone_number_contact function deletes a phone number from the contact.
    
    :param addressbook: AB: Pass the addressbook object to the function\n
    :param contact_name: str: Specify the name of the contact whose phone number is to be deleted\n
    :param phone_number: str: Identify the phone number that needs to be deleted
    """
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    phone_number = sanitize_phone_number(phone_number)
    phone = Phone(phone_number)
    check_phone_number_not_in_address_book(contact, phone, contact_name)

    contact.delete_phone_number(phone)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The phone number '{phone.phone}' was successfully deleted from the '{contact_name.title()}' contact.", fg='blue')


def add_email_to_contact(addressbook: AB,
                        contact_name: str,
                        contact_email: str) -> None:
    """
    The add_email_to_contact function adds an email to a contact in the address book.
    
    :param addressbook: AB: Pass in the addressbook object\n
    :param contact_name: str: Get the name of the contact you want to add an email to\n
    :param email: str: Pass the email address to be added to the contact
    """
    contact_name = contact_name.lower()
    contact_email = contact_email.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    email_validation(contact_email)
    email = Email(contact_email)

    check_email_in_address_book(contact, email, contact_name)

    contact.add_email(email)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The email '{email.email}' has been successfully added to the '{contact_name.title()}' contact.", fg='blue')


def change_email_contact(addressbook: AB,
                        contact_name: str,
                        contact_new_email: str,
                        contact_old_email: str) -> None:
    """
    The change_email_contact function takes in an addressbook, a contact name,
    a new email and an old email. It then checks if the contact name is not in the 
    address book. If it isn't then it will check if the old email is not in that 
    contact's list of emails. If it isn't then we verify that the new_email is valid 
    and create a new Email object with this value as its parameter. We also check to see 
    if this new_email already exists within our contacts list of emails and throw an error 
    message accordingly.
    
    :param addressbook: AB: Pass in the addressbook object\n
    :param contact_name: str: Get the contact name from the user\n
    :param new_email: str: Store the new email that will be added to the contact\n
    :param old_email: str: Specify the email that is to be changed
    """
    contact_name = contact_name.lower()
    contact_new_email = contact_new_email.lower()
    contact_old_email = contact_old_email.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    old_email = Email(contact_old_email)
    check_email_not_in_address_book(contact, old_email, contact_name)

    email_validation(contact_new_email)
    new_email = Email(contact_new_email)

    check_email_in_address_book(contact, new_email, contact_name)

    contact.change_email(old_email, new_email)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The contact '{contact_name.title()}' has been updated with the new email: {new_email.email}", fg='blue')


def delete_email_contact(addressbook: AB,
                        contact_name: str,
                        contact_email: str) -> None:
    """
    The delete_email_contact function deletes an email from a contact.
    
    :param addressbook: AB: Pass in the addressbook object\n
    :param contact_name: str: Get the contact name from the user\n
    :param email: str: Get the email address that will be deleted from the contact
    """
    contact_name = contact_name.lower()
    contact_email = contact_email.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)
    email = Email(contact_email)

    check_email_not_in_address_book(contact, email, contact_name)

    contact.delete_email(email)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The email '{email.email}' was successfully deleted from the '{contact_name.title()}' contact.", fg='blue')


def add_birthday_to_contact(addressbook: AB,
                            contact_name: str,
                            birthday_date: str) -> None:
    """
    The add_birthday_to_contact function adds a birthday to the contact.
    
    :param addressbook: AB: Specify the addressbook object that is being used\n
    :param contact_name: str: Identify the contact to add a birthday to\n
    :param birthday_date: str: Verify that the birthday date is valid
    """
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    birthday_date_validation(birthday_date)
    contact.add_birthday(birthday_date)

    addressbook.add_record(contact)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The birthday '{birthday_date}' has been added to the '{contact_name.title()}' contact.", fg='blue')


def change_birthday_contact(addressbook: AB,
                            contact_name: str,
                            new_birthday_date: str) -> None:
    """
    The change_birthday_contact function changes the birthday date of a contact in an address book.
    
    :param addressbook: AB: Pass in the addressbook object to the function\n
    :param contact_name: str: Specify the name of the contact whose birthday date is to be changed\n
    :param new_birthday_date: str: Pass the new birthday date to the function
    """
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    birthday_date_validation(new_birthday_date)
    contact.add_birthday(new_birthday_date)

    addressbook.add_record(contact)
    addressbook.save_records_to_file(FILE)
    click.secho(f"The birthday date for '{contact_name.title()}' has been changed to '{new_birthday_date}'.", fg='blue')


def serch_contact(addressbook: AB, criteria: str) -> None:
    """
    The serch_contact function searches for a contact in the address book.
          
    :param addressbook: AB: Specify the type of the parameter\n
    :param criteria: str: Specify the search criteria
    """
    criteria = criteria.lower()
    criteria_validation(criteria)

    result = addressbook.search(criteria)

    if isinstance(result, AB):
        print_all_contacts(result)
    else:
        click.echo(result)

    click.secho(f"{len(result)} contacts were found based on your search criteria!", fg='blue')


def print_all_contacts(addressbook: AB) -> str:
    """
    The print_all_contacts function prints all the contacts in the addressbook.
        It takes an AddressBook object as a parameter and returns nothing.
    
    :param addressbook: AB: Pass the addressbook object to the function
    """
    table = PrettyTable()
    table.field_names = ["Contact Name", "Phone Number", 'Email',
                            "Birthday", "Days to Birthday"]

    for contact in addressbook.values():
        contact_name = contact.user.name
        
        phone_numbers = [
            number.subrecord.phone for number in contact.phone_numbers] if contact.phone_numbers[0].subrecord.phone else '-'
        
        emails = [
            email.subrecord.email for email in contact.emails] if contact.emails[0].subrecord.email else '-'

        birthday = contact.user.birthday_date.strftime(
            '%d-%m-%Y') if contact.user.birthday_date else '-'
        
        day_to_birthday = contact.days_to_birthday() if contact.user.birthday_date else '-'

        table.add_row(
            [contact_name.title(), phone_numbers, emails, birthday, day_to_birthday])

    return f"{table}"
