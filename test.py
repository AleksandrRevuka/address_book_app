# python main.py -f sasha
# -a Olya 380956786543
# -c olya 380955436712 380956786543
# --add_phone olya 380956786543
# --add_birth olya 12-06-1985
# --change_birth olya 11-33-1980
# --change_birth olya 11-03-1980
# --change_birth olya 11-03-2030

# --add Alex 380964563456
# -c alex 380964563499 380964563456
# --add_phone alex 380675876987
# --add_phone alex 380964563456
# --del olya
# --del_phone alex 380964563499
# -c alex 380964563400 380964563456
# --add_birth alex 08-04-1985

# --add Alexq 380964563456
# --add Alexw 380964563456
# --add Alexe 380964563456
# --add Alexr 380964563456
# --add Alext 380964563456


from string import ascii_letters, digits
class Record:
    """ A class that represents a contact record in a phone book."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday_data = None

    def add_phone(self, phone):
        """Adds a new phone number to the contact."""
        self.phones.append(Phone(phone))
    
    def edit_phone(self, phone_number, new_phone_number):
        """Updates an existing phone number for the contact."""
        for phone in self.phones:
            if phone.phone == phone_number:
                phone.phone = new_phone_number
                break
    
    def delete_phone(self, phone_number):
        """Removes a phone number from the contact."""
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
        

user = Record("Alex")

user.add_phone("380634566576")
user.add_phone("380634566500")

user.edit_phone("380634566500", "380634560000")

for phone_user in user.phones:
    print(phone_user.phone)