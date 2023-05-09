"""..."""

import click
from click import Context

from constants import FILE
from address_book import AddressBook

# pass_addressbook = click.make_pass_decorator(AddressBook)

@click.group()
@click.pass_context
def bot(context: Context):
    address_book = AddressBook()
    address_book.read_records_from_file(FILE)
    context.obj = {'address_book': address_book}

@bot.command()
@click.option('--name', prompt=True)
@click.option('--phone', prompt=True, type=int)
@click.pass_obj
def add_phone(addressbook: Context, name, phone):
    click.echo(f'params {name}, {phone}!')
    print(addressbook)


@bot.command()
@click.option('--name', prompt=True)
@click.option('--phone', prompt=True, type=int)
@click.option('--old_phone', prompt=True, type=int)
@click.pass_obj
def change_phone(addressbook: Context, name, phone, old_phone):
    click.echo(f'params {name}, {phone}, and {old_phone}!')
    print(addressbook)


functions = {
    'add_phone': add_phone,
    'change_phone': change_phone,
}


@bot.command()
@click.option('--command', prompt=True, type=click.Choice(functions.keys()))
@click.pass_obj
def main(addressbook: Context, command):
    print('start')
    print(addressbook)
    functions[command]()


if __name__ == '__main__':
    bot()



# import click

# from address_book import Record, AddressBook as AB
# from entities import Phone, User
# from constants import  FILE

# # Default values:
# DFLT_DB_SCHEMA = "dhcp_snooping_schema.txt"


# def input_error(func):
#     """Decorator for handling input errors"""
#     def wrraper_input_error(*args, **kwargs):
#         """Wrapper function for handling input errors"""
#         try:
#             func(*args, **kwargs)

#         except TypeError as error:
#             print(f"TypeError: {error}")

#         except ValueError as error:
#             print(f"ValueError: {error}")

#         except KeyError as error:
#             print(f"KeyError: {error}")
            
#         finally:
#             close_bot()
        
#     return wrraper_input_error


# @click.group()
# @click.option("--ab-filename", default=FILE, help="db filename")
# @click.pass_context
# def main(context, ab_filename):
#     address_book = AB()
#     address_book.read_records_from_file(ab_filename)
#     context.obj = {'address_book': address_book}

# @main.command()
# @click.option("--db-schema", "-s", help="db schema filename")
# @click.pass_context
# def create(context):
#     """
#     create DB
#     """
#     user = context.obj['address_book']
#     print(user)
    
    
# @input_error
# @main.command()
# @click.option('--contact_name', '-cn', prompt=True, type=str)
# @click.option('--phone_number', '-pn', prompt=True, type=str)
# @click.pass_context
# def add_contact(context,
#                 contact_name: str,
#                 phone_number: str) -> str:
#     """Add a contact to the phone book."""
#     print(f"{contact_name}")
#     print(f"{context.obj['address_book']}")
#     if contact_name in context.obj['address_book']:
#         raise ValueError(
#             f"The contact '{contact_name.title()}' already exists in the address book.")
        
#     phone = Phone(phone_number)
#     user = User(contact_name)
#     contact = Record(user)
#     contact.add_phone_number(phone)
#     context.obj['address_book'].add_record(contact)
    
#     print(f"The contact '{contact_name.title()}' has been added: {phone.phone}")



# if __name__ == "__main__":
#     main()








# import click

# FILE = 'text.txt'

# @click.group()
# @click.option("--ab", default=FILE)
# @click.pass_context
# def main(context, db_filename):
#     context.obj = {"ab_filename": db_filename}
#     ...
    

# @main.command()
# @click.option('--name')
# @click.option('--phone', type=int)
# @click.pass_context
# def add(context, name, phone):
#     click.echo(f'params {name}, {phone}!')
#     print("Creating DB {} with DB schema {}".format(context.obj["ab_filename"], phone))


# if __name__ == '__main__':
#     main()
# type=click.Choice(functions.keys())
# import click

# click.echo(click.style('Hello World!', fg='blue'))
# click.echo(click.style('Some more text', bg='blue', fg='white'))
# click.echo(click.style('ATTENTION', blink=True, bold=True))


# @click.group()
# @click.option("--ab-filename", "-n", default=FILE, help="ab filename")
# @click.pass_context
# def main(address_book, ab_filename):
#     address_book.obj = {"ab_filename": ab_filename}


# def print_help(user_name: str) -> str:
#     """Print help for the console bot program."""
#     return f'{user_name}, this is help for the console bot program:\n{HELP}'


# @input_error
# @main.command()
# @click.option('--contact_name', '-cn')
# @click.option('--phone_number', '-pn', type=int)
# @click.pass_context
# def add_contact(address_book,
#                 contact_name: str,
#                 phone_number: str) -> str:
#     """Add a contact to the phone book."""
#     if contact_name and phone_number:
#         if contact_name in address_book:
#             raise ValueError(
#                 f"The contact '{contact_name.title()}' already exists in the address book.")
#         phone = Phone(phone_number)
#         user = User(contact_name)
#         contact = Record(user)
#         contact.add_phone_number(phone)
#         address_book["ab_filename"].add_record(contact)
#     else:
#         return "After the command, you must enter the new contact's name and phone number separated by a space.\nFor example: 'Smith 380631234567'"
    
#     return f"The contact '{contact_name.title()}' has been added: {phone.phone}"