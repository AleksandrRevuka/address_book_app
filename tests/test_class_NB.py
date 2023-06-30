"""Test class NoteBook"""
import unittest
from datetime import datetime

from my_address_book.entities import Note
from my_address_book.notes_book import NotesBook as NB
from my_address_book.records import RecordNote


class TestNotesBook(unittest.TestCase):
    """Tests class NotesBook"""

    def setUp(self) -> None:
        self.notesbook_test = NB()
        self.note_test = Note("some text")
        self.record_test = RecordNote(self.note_test)
        self.record_test.add_note_name("name note")

    def tearDown(self) -> None:
        del self.notesbook_test
        del self.record_test

    def test_add_record(self) -> None:
        """
        The test_add_record function tests the add_record function in NotesBook.py
            by adding a record to the notesbook and then checking if it was added correctly.
        """
        self.notesbook_test.add_record(self.record_test)
        record_note: RecordNote = self.notesbook_test.get_record("1")
        self.assertEqual(record_note.note.name_note, "name note")

    def test_search_note(self) -> None:
        """
        The test_search_note function tests the search function in NotesBook.py
            It creates a new record and adds it to the notesbook_test object, then searches in that object.
            The test passes if some text is found within the note of record_note.
        """
        self.notesbook_test.add_record(self.record_test)
        notesbook_search = self.notesbook_test.search("some")
        record_note: RecordNote = notesbook_search.get_record("1")
        note = record_note.note.note
        self.assertTrue("some text" in note)

    def test_search_name_note(self) -> None:
        """
        The test_search_name_note function tests the search function of the NotesBook class.
        It creates a new RecordNote object and adds it to a NotesBook object.
        Then, it searches for name in that notesbook and checks if the name of the note is found.
        """
        self.notesbook_test.add_record(self.record_test)
        notesbook_search = self.notesbook_test.search("name")
        record_note: RecordNote = notesbook_search.get_record("1")
        note_name = record_note.note.name_note
        self.assertTrue("name note" in note_name)

    def test_search_none(self) -> None:
        """
        The test_search_none function tests the search function of NotesBook.py
            by searching for a string that is not in any of the notesbook's records.
            The test passes if the length of notesbook_search is 0.
        """
        self.notesbook_test.add_record(self.record_test)
        notesbook_search = self.notesbook_test.search("none")
        self.assertTrue(0 == len(notesbook_search))

    def test_serch_date_of_creation(self) -> None:
        """
        The test_serch_date_of_creation function tests the search function of NotesBook class.
        It checks if the date_of_creation is in record note.
        """
        self.notesbook_test.add_record(self.record_test)
        current_date = datetime.now()
        time = current_date.strftime("%d-%m-%Y %H:%M")
        notesbook_search = self.notesbook_test.search(time)
        record_note: RecordNote = notesbook_search.get_record("1")
        self.assertTrue(time in record_note.date_of_creation)


if __name__ == "__main__":
    unittest.main()
