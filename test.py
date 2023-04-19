from collections import UserDict


class AddressBook(UserDict):
    """..."""

    def get_contact(self, name):
        """..."""
        return self.data[name]
    
    def add_record(self, record):
        """..."""
        self.data[record.name.value] = record
    
    def delete_record(self, record_name):
        """..."""
        del self.data[record_name]
    
    def search(self):
        """..."""
        pass


class Record:
    """..."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """..."""
        self.phones.append(Phone(phone))
    
    def edit_phone(self, phone_number, new_phone_number):
        """..."""
        for phone in self.phones:
            if phone.value == phone_number:
                phone.value = new_phone_number
                break
    
    def delete_phone(self, phone_number):
        """..."""
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break


class Field:
    """..."""
    def __init__(self, value):
        self.value = value


class Name(Field):
    """..."""
    pass


class Phone(Field):
    """..."""
    pass


name_con = Record('Sasha')

print(name_con.name.value)

name_con.add_phone('+380633512650')
name_con.add_phone('+380503512255')
# for number in name_con.phones:
#     print(number.value)
# print('==================================')
# name_con.edit_phone('+380633512650', '+380633332211')
# name_con.add_phone('+380633512650')

# for number in name_con.phones:
#     print(number.value)
# print('==================================')
# name_con.delete_phone('+380633512650')
# for number in name_con.phones:
#     print(number.value)


name_con_1 = Record('Olya')
name_con_1.add_phone('+380333512650')
name_con_1.add_phone('+380333666778')

phone_book = AddressBook()

phone_book.add_record(name_con)
phone_book.add_record(name_con_1)

contact = phone_book.get_contacts('Olya')


print([number.value for number in contact.phones])

# for contact in contacts:
#     name = contact.name.value
#     phones = [phone.value for phone in contact.phones]
#     print(f"{name}: {', '.join(phones)}")


def add_number_phone_to_contact(your_name: str, name: str, phone: str) -> str:
    """..."""
    if name not in phone_book:
        raise KeyError(f"Contact {name} not found")

    if len(phone.strip(digits + '+')) != 0:
        raise TypeError("Contact's phone can only contain digits")

    if len(phone) not in PHONE_RANGE:
        raise ValueError(
            f"Contact's phone {phone} is too long or short, it must be between 11 and 16 numbers")

    contact = phone_book.get_contact(name)
    contact.add_phone(phone)

    return f"{your_name}, {name}'s new contact phone {phone} has been successfully added to the address book"




elif command in ('--add_phone'):
    if name and phone:
        phone = sanitize_phone_number(phone)
        print(add_number_phone_tocontact(firstname, name, phone))
    else:
        print(f"After the command {command} you must enter the existing contact's name and new number with a space\nFor example: {command} Smith 380631234567")
