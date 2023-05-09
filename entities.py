"""entities"""

from datetime import datetime


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
        self.__name = new_name.lower()

    @property
    def birthday_date(self):
        """Returns the birthday date of the contact."""
        return self.__birthday_date

    @birthday_date.setter
    def birthday_date(self, new_birthday_date: str) -> None:
        """Sets the birthday date of the contact if it is valid, otherwise raises an error."""
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
        return ''.join(number.strip().strip('(, ), -, +, x, .') for number in phone)
