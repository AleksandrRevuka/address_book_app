
from datetime import datetime
from typing import Union, Any, List
from collections import UserDict

from my_address_book.entities import Phone, User, Email


class Book(UserDict):
    """..."""
    def get_record(self, name: str) -> 'Record':
        pass

    def add_record(self, record: 'Record') -> None:
        pass

    def delete_record(self, record_name: str) -> None:
        pass

    def sort_addressbook(self) -> None:
        pass
        
    def search(self, criteria: str):
        """..."""
        pass
        
    def save_records_to_file(self, file_name: str) -> None:
        pass

    def read_records_from_file(self, file_name: str) -> None:
        pass
    
    
class AddressBook(Book):

    def search(self, criteria: str) -> Union[str, 'AddressBook']:
        pass


class NotesBook(Book):

    def search(self, criteria: str) -> Union[str, 'NotesBook']:
        pass

class RecordNote:

    def __init__(self, note: 'Note'):
        self.note = note


class Record:

    class Subrecord:


        def __init__(self, subrecord: Any, name_subrecord: list | None):
            self.name = name_subrecord
            self.subrecord = subrecord

    def __init__(self, user: User):
        self.user = user
        self.phone_numbers: List['Record.Subrecord'] = []
        self.emails: List['Record.Subrecord'] = []

    def add_phone_number(self, phone_number: Phone, phone_assignment: list | None = None) -> None:
        pass

    def add_email(self, email: Email, email_assignment: list | None = None) -> None:
        pass

    def add_birthday(self, birthday_date: datetime) -> None:
        pass

    def days_to_birthday(self, current_date: Union[datetime, None] = None) -> Union[int, None]:
        pass


class Email:

    def __init__(self, email: str | None = None):
        self.email: str = email

    @property
    def email(self) -> str | None:
        pass

    @email.setter
    def email(self, new_email: str) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        pass


class User:

    def __init__(self, name: str | None = None):
        self.__birthday_date: date | None = None
        self.name: str = name

    @property
    def name(self) -> str | None:
        pass

    @name.setter
    def name(self, new_name: str) -> None:
        pass

    @property
    def birthday_date(self) -> date | None:
        pass

    @birthday_date.setter
    def birthday_date(self, new_birthday_date: datetime) -> None:
        pass


class Phone:

    def __init__(self, phone: str | None = None):
        self.phone: str = phone

    @property
    def phone(self) -> str | None:
        pass

    @phone.setter
    def phone(self, new_phone: str) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        pass


class Note:

    def __init__(self, note: str | None = None):
        self.note: str = note

    @property
    def note(self) -> str | None:
        pass

    @note.setter
    def phone(self, new_note: str) -> None:
        pass