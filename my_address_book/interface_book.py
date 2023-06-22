"""..."""
import pickle
from collections import UserDict
from abc import ABCMeta, abstractmethod

from my_address_book.records import RecordNote, RecordContact


class IBook(UserDict, metaclass=ABCMeta):
    """Interface Book"""
    @abstractmethod
    def get_record(self, name: str):
        pass

    @abstractmethod
    def delete_record(self, record_name: str):
        pass

    @abstractmethod
    def sort_book(self) -> None:
         pass

    @abstractmethod
    def save_records_to_file(self, file_name: str):
        pass

    @abstractmethod
    def read_records_from_file(self, file_name: str):
        pass


class Book(IBook):
    """
    This class represents an address book.

    Methods:
        get_record(name: str) -> RecordNote | Record:
            Returns the contact record for the given name.
        delete_record(record_name: str | int) -> None:
            Removes a contact record from the book.
        sort_book() -> None:
            Sorts the address book by name.
        save_records_to_file(file_name: str) -> None:
            Saves the data in the address book to a binary file using pickle.
        read_records_from_file(file_name: str) -> None:
            Reads data from a binary file using pickle and updates the address book.
    """
    def get_record(self, name: str) -> RecordNote | RecordContact:
        """
        Returns the contact record for the given name.
        """
        return self.data[name]

    def delete_record(self, record_name: str | int) -> None:
        """
        Removes a contact record from the book.
        """
        del self.data[record_name]

    def sort_book(self) -> None:
        """
        The sort_addressbook function sorts the address book by name.
        """
        self.data = dict(sorted(self.data.items(), key=lambda x: x[0]))

    def save_records_to_file(self, file_name: str) -> None:
        """
        Save the data in the address book to a binary file using pickle.
        """
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def read_records_from_file(self, file_name: str) -> None:
        """
        Read data from a binary file using pickle and update the address book.
        """
        try:
            with open(file_name, "rb") as file:
                content = pickle.load(file)
                self.data.update(content)
        except FileNotFoundError as error:
            raise FileNotFoundError(f"File not found {file_name}") from error
