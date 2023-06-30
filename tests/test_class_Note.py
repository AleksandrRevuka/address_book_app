"""Tests class Note"""
import unittest

from my_address_book.entities import Note


class TestNote(unittest.TestCase):
    """Tests class Note"""

    def setUp(self) -> None:
        self.note_test = Note("some text")
        self.note_test_none = Note()
        self.note_test.name_note = "name note"

    def tearDown(self) -> None:
        del self.note_test
        del self.note_test_none

    def test_set_note(self) -> None:
        """
        The test_set_note function tests the set_note function in the Note class.
        It does this by creating a new instance of the Note class, and then calling
        the set_note function on that instance. It then checks to see if it was
        successful by comparing what is stored in note with &quot;some text&quot;. If they are
        equal, it passes.
        """
        self.assertEqual(self.note_test.note, "some text")

    def test_set_note_none(self) -> None:
        """
        The test_set_note_none function tests the set_note function in the Note class.
        It checks to see if a note can be set to None.
        """

        self.assertEqual(self.note_test_none.note, None)

    def test_set_name_note(self) -> None:
        """
        The test_set_name_note function tests the set_name_note function in the Note class.
        It checks that when a name is passed to the set_name_note function, it sets self.name to that value.
        """
        self.assertEqual(self.note_test.name_note, "name note")


if __name__ == "__main__":
    unittest.main()
