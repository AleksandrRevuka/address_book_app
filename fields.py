"""field"""

from datetime import datetime
from string import ascii_letters, digits


class Name:
    """Represents the name of a contact."""

    def __init__(self, name):
        self.__name = None
        self.name = name

    @property
    def name(self):
        """Returns the name of the contact."""
        return self.__name

    @name.setter
    def name(self, new_name):
        """Sets the name of the contact if it is valid, otherwise raises an error."""
        self.__check = DataVerify
        self.__check.verify_name(new_name)
        self.__name = new_name


class Phone:
    """Represents the phone number of a contact."""

    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        """Returns the phone number of the contact."""
        return self.__phone

    @phone.setter
    def phone(self, new_phone):
        """Sets the phone number of the contact if it is valid, otherwise raises an error."""
        self.__check = DataVerify
        self.__check.verify_phone(new_phone)
        sanitize_phone = self.sanitize_phone_number(new_phone)
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
    def sanitize_phone_number(phone) -> str:
        """Clean number"""
        return ''.join(number.strip(' , (, ), -, +') for number in phone)


class Birthday:
    """Represents the birthday date of a contact."""

    def __init__(self, birthday_date):
        self.__birthday_date = None
        self.birthday_date = birthday_date

    @property
    def birthday_date(self):
        """Returns the birthday date of the contact."""
        return self.__birthday_date

    @birthday_date.setter
    def birthday_date(self, new_birthday_date):
        """Sets the birthday date of the contact if it is valid, otherwise raises an error."""
        self.__check = DataVerify
        self.__check.verify_birthday_data(new_birthday_date)
        self.__birthday_date = datetime.strptime(
            new_birthday_date, '%d-%m-%Y').date()


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
    def verify_birthday_data(cls, birthday_data):
        """Verifies a birthday data."""
        try:
            birthday_data = datetime.strptime(birthday_data, '%d-%m-%Y')
        except ValueError as error:
            raise ValueError(
                f"Incorrect date format: '{birthday_data}', should be in the format DD-MM-YYYY") from error

        if birthday_data >= datetime.now():
            raise ValueError(
                f"Birthday '{birthday_data.date()}' must be in the past")
