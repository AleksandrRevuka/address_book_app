"""Test RecordNote"""
import unittest
from datetime import datetime

from my_address_book.entities import Note
from my_address_book.records import RecordNote


class TestRecordNote(unittest.TestCase):
    """Tests class Record"""

    def setUp(self) -> None:
        self.note_test: Note = Note("some text")
        self.record_test: RecordNote = RecordNote(self.note_test)

    def tearDown(self) -> None:
        del self.note_test
        del self.record_test

    def test_add_note(self) -> None:
        new_note: str = "new note"
        self.record_test.add_note(new_note)
        self.assertEqual(self.record_test.note.note, "new note")

    def test_add_name_note(self) -> None:
        self.record_test.add_note_name("name note")
        self.assertEqual(self.record_test.note.name_note, "name note")

    def test_make_date_of_creation(self) -> None:
        current_date = datetime.now()
        time = current_date.strftime("%d-%m-%Y %H:%M")
        self.assertTrue(time in self.record_test.date_of_creation)
