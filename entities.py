"""entities"""
import re

from datetime import datetime
from string import ascii_letters, digits


class Email:
    """..."""
    def __init__(self, email: str):
        self.__email = None
        self.email = email

    @property
    def email(self) -> str:
        """Returns the phone number of the contact."""
        return self.__email

    @email.setter
    def email(self, new_email: str) -> None:
        """
        The email function takes in a string and checks to see if it is a valid email address.
            If the email address is not valid, an error message will be returned.
            If the email address is valid, then it will return True.
        """
        self.__check = DataVerify
        self.__check.verify_email(new_email)
        self.__email = new_email

    def __eq__(self, other: object) -> bool:
        return self.email == other.email


class User:
    """..."""
    def __init__(self, name: str):
        self.__name = None
        self.__birthday_date = None
        self.name = name

    @property
    def name(self):
        """Returns the name of the contact."""
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        """Sets the name of the contact if it is valid, otherwise raises an error."""
        self.__check = DataVerify
        self.__check.verify_name(new_name)
        self.__name = new_name

    @property
    def birthday_date(self):
        """Returns the birthday date of the contact."""
        return self.__birthday_date

    @birthday_date.setter
    def birthday_date(self, new_birthday_date: str) -> None:
        """Sets the birthday date of the contact if it is valid, otherwise raises an error."""
        self.__check = DataVerify
        self.__check.verify_birthday_date(new_birthday_date)
        self.__birthday_date = datetime.strptime(
            new_birthday_date, '%d-%m-%Y').date()

class Phone:
    """Represents the phone number of a contact."""
    def __init__(self, phone: str):
        self.__phone = None
        self.phone = phone
        
    # def __repr__(self):
    #         return self.phone

    @property
    def phone(self):
        """Returns the phone number of the contact."""
        return self.__phone

    @phone.setter
    def phone(self, new_phone: str) -> None:
        """Sets the phone number of the contact if it is valid, otherwise raises an error."""
        sanitize_phone = self.sanitize_phone_number(new_phone)
        self.__check = DataVerify
        self.__check.verify_phone(sanitize_phone)
        self.__phone = sanitize_phone

    def __eq__(self, other: object) -> bool:
        return self.phone == other.phone

    @staticmethod
    def format_phone_number(func):
        """Add '+' to phone's number"""
        def add_code_phone(phone):
            phone = func(phone)
            return ''.join('+' + phone)

        return add_code_phone

    @staticmethod
    @format_phone_number
    def sanitize_phone_number(phone: str) -> str:
        """Clean number"""
        return ''.join(number.strip('(, ), -, +') for number in phone)
            
            
class DataVerify:
    """A utility class for verifying contact data"""

    CYRILLIC = 'абвгґдеєёжзиіїйклмнопрстуфхцчшщъыьэюя'
    LETTERS = ascii_letters + CYRILLIC + CYRILLIC.upper()
    NAME_RANGE = range(1, 50)
    PHONE_RANGE = range(11, 17)

    @classmethod
    def verify_name(cls, name: str):
        """Verifies that the input string `name` is a valid name for a contact."""

        if not isinstance(name, str):
            raise TypeError(
                f"Name must be a string, but got {type(name).__name__}")

        if len(name.strip(cls.LETTERS)) != 0:
            raise TypeError(
                f"Contact's name can only contain letters, but got '{name.title()}'")

        if len(name) not in cls.NAME_RANGE:
            raise ValueError(
                f"Name length must be between {cls.NAME_RANGE[0]} and {cls.NAME_RANGE[-1]}, but got '{name.title()}'")

    @classmethod
    def verify_phone(cls, phone: str):
        """Verifies a phone number."""

        if len(phone.strip(digits + '+')) != 0:
            raise TypeError(
                f"Contact's phone can only contain digits, but got '{phone}'")

        if len(phone) not in cls.PHONE_RANGE:
            raise ValueError(
                f"Contact's phone must be between 11 and 16 numbers, but got '{phone}'")

    @classmethod
    def verify_birthday_date(cls, birthday_data: str):
        """Verifies a birthday data."""
        try:
            birthday_data = datetime.strptime(birthday_data, '%d-%m-%Y')
        except ValueError as error:
            raise ValueError(
                f"Incorrect date format: '{birthday_data}', should be in the format DD-MM-YYYY") from error

        if birthday_data >= datetime.now():
            raise ValueError(
                f"Birthday '{birthday_data.date()}' must be in the past")

    @classmethod
    def verify_email(cls, email: str):
        """Verifies an email address."""
        pattern = r"[a-zA-Z][a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        if not re.match(pattern, email):
            raise ValueError(f"Invalid '{email}' email address.")