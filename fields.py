"""field"""

from datetime import datetime 
from string import ascii_letters, digits

class Field:
    """..."""
    def __init__(self, value):
        self.value = value


class Name(Field):
    """..."""
    def __init__(self, name):
        super().__init__(name)
        self.__name = None
        self.name = name

    @property
    def name(self):
        """..."""
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__check = DataVerify
        self.__check.verify_name(new_name)
        self.__name = new_name

class Phone(Field):
    """..."""
    def __init__(self, phone):
        super().__init__(phone)
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        """..."""
        return self.__phone

    @phone.setter
    def phone(self, new_phone):
        self.__check = DataVerify
        self.__check.verify_phone(new_phone)
        self.__phone = new_phone


class Birthday(Field):
    """..."""
    def __init__(self, birthday_data):
        super().__init__(birthday_data)
        self.__birthday_data = None
        self.birthday_data = birthday_data

    @property
    def birthday_data(self):
        """..."""
        return self.__birthday_data

    @birthday_data.setter
    def birthday_data(self, new_birthday_data):
        self.__check = DataVerify
        self.__check.verify_birthday_data(new_birthday_data)
        self.__birthday_data = datetime.strptime(new_birthday_data, '%d-%m-%Y').date()

class DataVerify:
    """..."""
    CYRILLIC = 'абвгґдеєёжзиіїйклмнопрстуфхцчшщъыьэюя'
    LETTERS = ascii_letters + CYRILLIC + CYRILLIC.upper()
    NAME_RANGE = range(1, 50)
    PHONE_RANGE = range(11, 17)

    @classmethod
    def verify_name(cls, name: str):
        """Verifies that the input string `name` is a valid name for a contact."""

        if not isinstance(name, str):
            raise TypeError(f"Name '{name.title()}' must be a string")

        if len(name.strip(cls.LETTERS)) != 0:
            raise TypeError(f"Contact's name '{name.title()}' can only contain letters")
        
        if len(name) not in cls.NAME_RANGE:
            raise ValueError(f"Name '{name.title()}' length must be between {cls.NAME_RANGE[0]} and {cls.NAME_RANGE[-1]}")

    @classmethod
    def verify_phone(cls, phone: str):
        """Verifies a phone number."""

        if len(phone.strip(digits + '+')) != 0:
            raise TypeError(f"Contact's phone '{phone}' can only contain digits")

        if len(phone) not in cls.PHONE_RANGE:
            raise ValueError(
                f"Contact's phone '{phone}' is too long or short, it must be between 11 and 16 numbers")
        
    @classmethod
    def verify_birthday_data(cls, birthday_data):
        """Verifies a birthday data."""
        try:
            birthday_data = datetime.strptime(birthday_data, '%d-%m-%Y')
        except ValueError as error:
            raise ValueError("Incorrect data format '{birthday_data}', should be DD-MM-YYYY") from error
        
        if birthday_data >= datetime.now():
            raise ValueError(f"Birthday '{birthday_data.date()}' must be in the past")