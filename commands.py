"""commands"""

import click
from click import Context
from prettytable import PrettyTable

from verify_data import (
    verify_name,
    verify_phone,
    verify_email,
    verify_birthday_date,
    verify_criteria,
    check_name_in_address_book,
    check_name_not_in_address_book,
    check_phone_number_in_address_book,
    check_phone_number_not_in_address_book,
    check_email_in_address_book,
    check_email_not_in_address_book,
)
from constants import NUMBER_OF_CONTACTS_PER_PAGE, FILE
from address_book import Record, AddressBook as AB
from entities import Phone, User, Email


@click.group()
@click.option("--ab-filename", default=FILE, help="Addressbook filename")
@click.pass_context
def main(addressbook: Context, ab_filename: str):
    address_book = AB()
    address_book.read_records_from_file(ab_filename)
    addressbook.obj = address_book


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--phone_number', prompt=True, type=str)
@click.pass_obj
def add_contact(addressbook: AB,
                contact_name: str,
                phone_number: str):
    """Add a contact to the phone book."""
    check_name_in_address_book(addressbook, contact_name)
    verify_name(contact_name)

    phone = Phone(phone_number)
    user = User(contact_name)
    contact = Record(user)
    contact.add_phone_number(phone)
    addressbook.add_record(contact)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The contact '{contact_name.title()}' has been added: {phone.phone}", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.pass_obj
def print_contact(addressbook: AB, contact_name: str):
    """Print the phone number and other details of a contact from the phone book."""
    check_name_not_in_address_book(addressbook, contact_name)

    table = PrettyTable()
    table.field_names = ["Contact name", "Phone number",
                         "Email", "Birthday", "Days to Birthday"]

    contact = addressbook.get_contact(contact_name)
    phone_numbers = [
        number.subrecord.phone for number in contact.phone_numbers]
    emails = [email.subrecord.email for email in contact.emails]
    birthday = contact.user.birthday_date.strftime(
        '%d-%m-%Y') if contact.user.birthday_date else '-'
    day_to_birthday = contact.days_to_birthday() if contact.user.birthday_date else '-'
    table.add_row([contact_name.title(), phone_numbers,
                  emails, birthday, day_to_birthday])

    click.secho(f"{contact_name.title()}:\n{table}", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.pass_obj
def del_contact(addressbook: AB, contact_name: str):
    """Delete the phone number of a contact from the phone book."""
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    addressbook.delete_record(contact_name)
    addressbook.save_records_to_file(FILE)
    click.secho(f"The contact '{contact_name.title()}' has been deleted.", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--phone_number', prompt=True, type=str)
@click.pass_obj
def add_phone(addressbook: AB, contact_name: str, phone_number: str):
    """Adds a new phone number to an existing contact in the phone book."""
    contact_name = contact_name.lower()
    verify_phone(phone_number)
    phone = Phone(phone_number)

    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    check_phone_number_in_address_book(contact, phone, contact_name)

    contact.add_phone_number(phone)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The phone number '{phone.phone}' has been successfully added to the '{contact_name.title()}' contact.", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--new_phone_number', prompt=True, type=str)
@click.option('--old_phone_number', prompt=True, type=str)
@click.pass_obj
def change_phone(addressbook: AB,
                 contact_name: str,
                 new_phone_number: str,
                 old_phone_number: str):
    """Change the phone number of a contact in the phone book."""
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)
    contact = addressbook.get_contact(contact_name)

    verify_phone(old_phone_number)
    old_phone = Phone(old_phone_number)
    check_phone_number_not_in_address_book(contact, old_phone, contact_name)

    verify_phone(new_phone_number)
    new_phone = Phone(new_phone_number)
    check_phone_number_in_address_book(contact, new_phone, contact_name)

    contact.change_phone_number(old_phone, new_phone)
    addressbook.add_record(contact)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The contact '{contact_name.title()}' has been updated with the new phone number: {new_phone.phone}", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--phone_number', prompt=True, type=str)
@click.pass_obj
def del_phone(addressbook: AB,
              contact_name: str,
              phone_number: str):
    """Deletes a phone number from an existing contact in the address book."""
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    phone = Phone(phone_number)
    check_phone_number_not_in_address_book(contact, phone, contact_name)

    contact.delete_phone_number(phone)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The phone number '{phone.phone}' was successfully deleted from the '{contact_name.title()}' contact.", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--email', prompt=True, type=str)
@click.pass_obj
def add_email(addressbook: AB,
              contact_name: str,
              email: str):
    """
    The add_email function adds an email to a contact.
    """
    contact_name = contact_name.lower()
    email = email.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    verify_email(email)
    email = Email(email)

    check_email_in_address_book(contact, email, contact_name)

    contact.add_email(email)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The email '{email.email}' has been successfully added to the '{contact_name.title()}' contact.", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--new_email', prompt=True, type=str)
@click.option('--old_email', prompt=True, type=str)
@click.pass_obj
def change_email(addressbook: AB,
                 contact_name: str,
                 new_email: str,
                 old_email: str):
    """
    The change_email function changes the email of a contact in an address book.
    """
    contact_name = contact_name.lower()
    new_email = new_email.lower()
    old_email = old_email.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    old_email = Email(old_email)
    check_email_not_in_address_book(contact, old_email, contact_name)

    verify_email(new_email)
    new_email = Email(new_email)

    check_email_in_address_book(contact, new_email, contact_name)

    contact.change_email(old_email, new_email)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The contact '{contact_name.title()}' has been updated with the new email: {new_email.email}", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--email', prompt=True, type=str)
@click.pass_obj
def del_email(addressbook: AB,
              contact_name: str,
              email: str):
    """
    The delete_email function deletes the email from the contact.
    """
    contact_name = contact_name.lower()
    email = email.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)
    email = Email(email)

    check_email_not_in_address_book(contact, email, contact_name)

    contact.delete_email(email)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The email '{email.email}' was successfully deleted from the '{contact_name.title()}' contact.", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--birthday_date', prompt=True, type=str)
@click.pass_obj
def add_birthday(addressbook: AB,
                 contact_name: str,
                 birthday_date):
    """Adds a birthday date to an existing contact in the phone book."""
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    verify_birthday_date(birthday_date)
    contact.add_birthday(birthday_date)

    addressbook.add_record(contact)
    addressbook.save_records_to_file(FILE)
    click.secho(
        f"The birthday '{birthday_date}' has been added to the '{contact_name.title()}' contact.", fg='blue')


@main.command()
@click.option('--contact_name', prompt=True, type=str)
@click.option('--new_birthday_date', prompt=True, type=str)
@click.pass_obj
def change_birthday(addressbook: AB,
                    contact_name: str,
                    new_birthday_date):
    """Changes the birthday date of an existing contact in the phone book."""
    contact_name = contact_name.lower()
    check_name_not_in_address_book(addressbook, contact_name)

    contact = addressbook.get_contact(contact_name)

    verify_birthday_date(new_birthday_date)
    contact.add_birthday(new_birthday_date)

    addressbook.add_record(contact)
    addressbook.save_records_to_file(FILE)
    click.secho(f"The birthday date for '{contact_name.title()}' has been changed to '{new_birthday_date}'.", fg='blue')


@main.command()
@click.option('--criteria', prompt=True, type=str)
@click.pass_obj
def serch_contact(addressbook: AB, criteria: str):
    """Search for contacts in an address book based on a given criteria and print the results."""
    criteria = criteria.lower()
    verify_criteria(criteria)

    result = addressbook.search(criteria)

    if isinstance(result, AB):
        print_all_contacts(result)
    else:
        click.echo(result)

    click.secho(f"{len(result)} contacts were found based on your search criteria!", fg='blue')


@main.command()
@click.pass_obj
def print_contacts(addressbook: AB):
    """Print all contacts from the phone book."""
    print_all_contacts(addressbook)


def print_all_contacts(addressbook: AB):
    """Print all contacts from the phone book."""

    for i, contacts in enumerate(addressbook.record_iterator(NUMBER_OF_CONTACTS_PER_PAGE), 1):
        table = PrettyTable()
        table.field_names = ["Contact Name", "Phone Number", 'Email',
                             "Birthday", "Days to Birthday"]

        for contact in contacts:
            contact_name = contact.user.name
            phone_numbers = [
                number.subrecord.phone for number in contact.phone_numbers]
            emails = [email.subrecord.email for email in contact.emails]

            birthday = contact.user.birthday_date.strftime(
                '%d-%m-%Y') if contact.user.birthday_date else '-'
            day_to_birthday = contact.days_to_birthday() if contact.user.birthday_date else '-'

            table.add_row(
                [contact_name.title(), phone_numbers, emails, birthday, day_to_birthday])

        click.secho(f"This is page {i} of your phone book:", fg='yellow')
        click.secho(f"{table}", bg='green', fg='black')

    click.secho("End of contacts.", fg='blue')


if __name__ == "__main__":
    main()
