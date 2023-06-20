"""
...
"""
import re
from typing import Union
from abc import ABC, abstractmethod

from my_address_book.interface_book import Book
from my_address_book.records import RecordNote
from my_address_book.constants import PUNCTUATION


class INotesBook(ABC):
    """Interface NotesBook"""

    @abstractmethod
    def add_record(self, record: RecordNote):
        pass

    @abstractmethod
    def search(self, criteria: str):
        pass


class NotesBook(Book, INotesBook):
    """
    A class that represents a notes book containing note records.

    Methods:
        add_record(record: 'RecordNote') -> None:
            Adds a new note record to the notes book.
        search(criteria: str) -> Union[str, 'NotesBook']:
            Performs a search for notes based on the given criteria.
        note_number() -> str:
            Generates a new note number for adding a note to the book.
        re_numbering() -> None:
            Re-numbers the note records in the book to ensure sequential numbering.
    """

    def add_record(self, record: 'RecordNote') -> None:
        """
        Adds a new note record to the notes book.
        """
        note_num: str = self.note_number()
        self.data[note_num] = record

    def search(self, criteria: str) -> Union[str, 'NotesBook']:
        search_notes = NotesBook()
        
        if criteria[0] not in PUNCTUATION:
            for record in self.data.values():
                
                if re.search(criteria.lower(), record.note.note.lower()):
                    search_notes.add_record(record)
                    
                if re.search(criteria.lower(), record.note.name_note.lower()):
                    search_notes.add_record(record)
                    
                if re.search(criteria, record.date_of_creation):
                    search_notes.add_record(record)
        
        return search_notes

    def note_number(self) -> str:
        """
        The note_number function is used to number the notes in a notebook.
        It takes the length of the data list and adds 1 to it, returning that value as a string.
        """

        self.re_numbering()
        length_notesbook = len(self.data)
        return str(length_notesbook + 1)

    def re_numbering(self) -> None:
        """
        The re_numbering function takes a dictionary of records and re-numbers the keys in order.
        This is useful when deleting records, as it ensures that there are no gaps in the numbering.
        """

        keys = list(self.data)
        records = list(self.data.values())
        new_keys = list(map(str, range(1, len(keys) + 1)))
        self.data = dict(zip(new_keys, records))
