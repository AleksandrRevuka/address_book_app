"""Record"""
from datetime import date
from datetime import datetime
from typing import Any
from typing import Union

from my_address_book.entities import Email
from my_address_book.entities import Note
from my_address_book.entities import Phone
from my_address_book.entities import User


class RecordNote:
    """
    A class that represents a record of a note.

    Attributes:
        note (Note): The note object associated with the record.
        date_of_creation (datetime): The date of creation of the record.

    Methods:
        add_note_name(note_name: str) -> None:
            Adds a name to the note object.
        add_note(note_new: str) -> None:
            Adds a note to the note object.
        make_date_of_creation() -> datetime:
            Creates and returns the current date as the date of creation.
    """

    def __init__(self, note: Note):
        self.note: Note = note
        self.date_of_creation: str = self.make_date_of_creation()

    def add_note_name(self, note_name: str) -> None:
        """
        The add_note_name function adds a note name to the note object.
        """

        self.note.name_note = note_name

    def add_note(self, note_new: str) -> None:
        """
        The add_note function adds a note to the user's profile.
        """

        self.note.note = note_new

    def make_date_of_creation(self) -> str:
        """
        The make_date_of_creation function creates a date of creation for the user.
        The function takes in no arguments and returns the current date.
        """

        current_date = datetime.now()
        return current_date.strftime("%d-%m-%Y %H:%M:%S")


class RecordContact:
    """
    Record is a class that represents a contact record in a phone book.

    This class stores information about a contact, including user details, phone numbers, and emails.

    Attributes:
        user (User): The User object representing the user details of the contact.
        phone_numbers (List[Record.Subrecord]): A list of Subrecord objects representing the phone numbers of
        the contact.
        emails (List[Record.Subrecord]): A list of Subrecord objects representing the emails of the contact.

    Methods:
        add_phone_number: Adds a new phone number to the contact.

        add_email: Adds a new email to the contact.

        add_birthday: Adds a birthday date to the contact.

        days_to_birthday: Calculates the number of days until the next birthday of the contact.
    """

    class Subrecord:
        """
        Subrecord is a class representing a subrecord of a contact, such as a phone number or email.

        Attributes:
            name (List[str] | None): The name associated with the subrecord.
            subrecord (Any): The subrecord data.
        """

        def __init__(self, subrecord: Any, name_subrecord: list | None):
            self.name = name_subrecord
            self.subrecord = subrecord

    def __init__(self, user: User):
        self.user = user
        self.phone_numbers: list["RecordContact.Subrecord"] = []
        self.emails: list["RecordContact.Subrecord"] = []

    def add_phone_number(self, phone_number: Phone, phone_assignment: list | None = None) -> None:
        """
        Adds a new phone number to the contact.
        """
        subrecord_phone = self.Subrecord(phone_number, phone_assignment)
        self.phone_numbers.append(subrecord_phone)

    def add_email(self, email: Email, email_assignment: list | None = None) -> None:
        """
        Adds a new email to the contact.
        """
        subrecord_email = self.Subrecord(email, email_assignment)
        self.emails.append(subrecord_email)

    def add_birthday(self, birthday_date: datetime) -> None:
        """
        Add a birthday data to the contact.
        """
        self.user.birthday_date = birthday_date

    def days_to_birthday(self, current_date: Union[datetime, None] = None) -> Union[int, None]:
        """
        Calculate the number of days to the next birthday.
        """
        if current_date is None:  # this check is required for the test
            current_date = datetime.now()

        birthday = self.user.birthday_date

        if isinstance(birthday, date):
            next_birthday = datetime(current_date.year, birthday.month, birthday.day)

            if next_birthday < current_date:
                next_birthday = datetime(current_date.year + 1, birthday.month, birthday.day)
        else:
            return None

        return (next_birthday - current_date).days
