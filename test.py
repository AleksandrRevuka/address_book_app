# python main.py -f sasha
# -a Olya 380956786543
# -c olya 380955436712 380956786543
# --add_phone olya 380956786543
# --add_birth olya 12-06-1985
# --change_birth olya 11-33-1980
# --change_birth olya 11-03-1980
# --change_birth olya 11-03-2030
# --print olya

# --add Alex 380964563456
# -c alex 380964563499 380964563456
# --add_phone alex 380675876987
# --add_phone alex 380964563456
# --del olya
# --del_phone alex 380964563499
# -c alex 380964563400 380964563456
# --add_birth alex 08-04-1985
# -p alex

# --add Alexq 380964563456
# --add Alexw 380964563456
# --add Alexe 380964563456
# --add Alexr 380964563456
# --add Alext 380964563456


# --add Анастасія +1650-253-0000
# --add Олександр +442070313000
# --add Юлія +33142681000
# --add Ігор +912222785000
# --add Марія +813-5250-6500
# --add Віктор +861084088000
# --add Надія +493030808000
# --add Тетяна +55114003-1000
# --add Дмитро +61293744000

# --add_birth Юлія 12-06-1993
# --add_birth Марія 29-05-1992
# --add_birth Віктор 08-08-1991
# --add_birth Надія 17-11-1990
# --add_birth Дмитро 25-01-1994
import unittest
from datetime import datetime
from unittest import TestCase, mock
class Record:
    """A class that represents a contact record in a phone book."""

    def __init__(self):
        self.birthday = None

    def add_birthday(self, birthday_date):
        """Add a birthday data to the contact."""
        self.birthday = Birthday(birthday_date)

    def days_to_birthday(self):
        """Calculate the number of days to the next birthday."""
        now = datetime.now()
        birthday = self.birthday.birthday_date
        next_birthday = datetime(now.year, birthday.month, birthday.day)
        if next_birthday < now:
            next_birthday = datetime(
                now.year + 1, birthday.month, birthday.day)

        return (next_birthday - now).days
    

class TestRecord(TestCase):
    """Tests class Record"""

    def setUp(self) -> None:
        self.record_test = Record()

    def test_days_to_birthday(self):
        current_date = datetime(2023, 1, 1)
        birthday_mock = mock.Mock()
        birthday_mock.birthday_date = datetime(2000, 6, 1)
        self.record_test.birthday = birthday_mock

        with mock.patch('datetime.datetime') as datetime_mock:
            datetime_mock.now.return_value = current_date

            self.assertEqual(self.record_test.days_to_birthday(), 153)

if __name__ == '__main__':
    unittest.main()