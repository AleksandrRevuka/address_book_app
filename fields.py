"""field"""

from string import ascii_letters, digits

class Field:
    """..."""
    def __init__(self, value):
        self.value = value


class Name(Field):
    """..."""
    def __init__(self, name):
        super().__init__(name)
        self.__check = DataVerify
        self.__check.verify_name(name)


class Phone(Field):
    """..."""
    def __init__(self, phone):
        super().__init__(phone)
        self.__check = DataVerify
        self.__check.verify_phone(phone)


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