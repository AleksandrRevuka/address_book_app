from my_address_book.utils import print_all_contacts
from my_address_book.entities import Phone, User, Email
from my_address_book.address_book import RecordContact, AddressBook as AB

addressbook_test = AB()
user_test = User('sasha')
phone_test = Phone('380951234567')
email_test = Email('test_sasha@gmail.com')
record_test = RecordContact(user_test)


addressbook_test.add_record(record_test)

result = print_all_contacts(addressbook_test)
print(result)