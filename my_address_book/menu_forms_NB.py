"""..."""
import npyscreen

from my_address_book.validation import check_number_not_in_notes_book, note_validation
from my_address_book.entities import Note
from my_address_book.records import RecordNote
from my_address_book.constants import FILE_NB


class EditNoteForm(npyscreen.ActionPopup):
    """
    This class represents a form for editing a note in the address book.

    Attributes:
        number_note_for_change (npyscreen.TitleText):
            The widget for entering the number of the note to be edited.

    Methods:
        create(): Sets up the form and its widgets.
        beforeEditing(): Initializes the form before it is edited.
        check_number_note(): Checks if the entered note number is valid.
        on_ok(): Called when the user presses OK on the form, performs validation and switches to the add note form.
        on_cancel(): Called when the user cancels the form, switches back to the main note form.
    """

    def create(self) -> None:
        """
        The create function is called once, when the form first comes to life.
        It should be used to create all of the widgets that will be displayed on the form.
        The function takes no arguments and returns nothing.
        """
        
        self.number_note_for_change = self.add(npyscreen.TitleText, name='Number note')

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data from your application.
        """
        
        self.number_note_for_change.value = None

    def check_number_note(self) -> bool:
        """
        The check_number_note function checks if the number of note is in notesbook.
        If it is, then the function returns False and a message appears on screen.
        Otherwise, it returns True.
        """
        
        name = self.number_note_for_change.value
        message = check_number_not_in_notes_book(self.parentApp.notesbook, name)
        if message:
            npyscreen.notify_confirm(message, "Error", editw=1)
            self.number_note_for_change.value = None
            return False
        return True

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses OK.
        It checks if the number of note is in notes book, and then it changes form to ADD NOTE with value from this form.
        """
        
        if self.check_number_note():
            self.parentApp.getForm('ADD NOTE').value = self.number_note_for_change.value
            self.parentApp.getForm('ADD NOTE').name = "Edit note"
            self.parentApp.switchForm('ADD NOTE')

    def on_cancel(self) -> None:
        """
        The on_cancel function is called when the user presses the cancel button.
        It will return to the previous form, which in this case is NOTE MAIN.
        """
        
        self.parentApp.switchForm("NOTE MAIN")


class DeleteNoteForm(npyscreen.ActionPopup):
    """
    This class represents a form for deleting a note from the address book.

    Attributes:
        number_note_for_del (npyscreen.TitleText):
            The widget for entering the number of the note to be deleted.

    Methods:
        create(): Sets up the form and its widgets.
        beforeEditing(): Initializes the form before it is edited.
        check_number_note(): Checks if the entered note number is valid.
        delete_contact(): Deletes the note from the address book.
        on_ok(): Called when the user presses OK on the form, performs validation and deletes the note.
        on_cancel(): Called when the user cancels the form, switches back to the main note form.
    """

    def create(self) -> None:
        """
        The create function is called once, when the form first comes to life.
        It should be used to create all of the widgets that will be displayed on the form.
        The function takes no arguments and returns nothing.
        """
        
        self.number_note_for_del = self.add(npyscreen.TitleText, name='Number note')

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to perform any actions that are required to prepare for the user's interaction with your form.
        For example, if you need to populate a list of choices from a database, this would be where you would do it.
        """
        
        self.number_note_for_del.value = None

    def check_number_note(self) -> bool:
        """
        The check_number_note function checks if the number of note is in notesbook.
        If it is not, then a message appears and the function returns False.
        Otherwise, it returns True.
        """
        
        number = self.number_note_for_del.value
        message = check_number_not_in_notes_book(self.parentApp.notesbook, number)
        if message:
            npyscreen.notify_confirm(message, "Error", editw=1)
            self.number_note_for_del.value = None
            return False
        return True

    def delete_contact(self) -> str:
        """
        The delete_contact function deletes a contact from the notesbook.
        """
        
        self.parentApp.notesbook.delete_record(self.number_note_for_del.value)
        self.parentApp.notesbook.save_records_to_file(FILE_NB)
        return f"The note '{self.number_note_for_del.value}' has been deleted."

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses OK.
        It will validate that the number entered is not already in use, and if it isn't,
        it will add a new contact to the database.
        """
        
        respon = self.check_number_note()
        if respon:
            message = self.delete_contact()
            npyscreen.notify_confirm(message, "Delete!", editw=1)

            self.parentApp.switchForm("NOTE MAIN")

    def on_cancel(self) -> None:
        """
        The on_cancel function is called when the user presses the cancel button.
        It will return to the previous form, which in this case is NOTE MAIN.
        """
        
        self.parentApp.switchForm("NOTE MAIN")


class AddNoteForm(npyscreen.ActionForm):
    """
    This class represents a form for adding or editing a note in the address book.

    Attributes:
        value (str): The value of the note being added or edited.
        wg_note_name (npyscreen.TitleText): The widget for entering the name of the note.
        wg_note (npyscreen.MultiLineEdit): The widget for entering the content of the note.

    Methods:
        create(): Sets up the form and its widgets.
        beforeEditing(): Initializes the form with existing note data.
        after_editing(): Resets the form after editing is done.
        data_validation(): Validates the entered note data.
        add_note(): Adds a new note to the address book.
        change_note(): Updates an existing note in the address book.
        on_ok(): Called when the user presses OK on the form, performs validation and adds/updates the note.
        on_cancel(): Called when the user cancels the form, resets the form and switches back to the main note form.
    """

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It should be used to create all of the widgets that will be displayed on the form, and to lay them out in
        a way that makes sense for your application.
        The function takes one argument: self, which refers to the Form object itself.
        """

        self.value = None
        self.wg_note_name: npyscreen.TitleText = self.add(npyscreen.TitleText, name='Note name:')
        self.wg_name: npyscreen.TitleFixedText = self.add(npyscreen.TitleFixedText, name='Note:', editable=False)
        self.wg_note: npyscreen.MultiLineEdit = self.add(npyscreen.MultiLineEdit)

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the values of widgets on your form, based on
        the state of your application or user input.  It also allows you to
        change which widgets are available for editing, and how they behave.
        """

        if self.value:
            record_note: RecordNote = self.parentApp.notesbook.get_record(self.value)

            self.wg_note_name.value = record_note.note.name_note
            self.wg_note.value = record_note.note.note

    def after_editing(self) -> None:
        """
        The after_editing function is called when the user presses ENTER on a widget.
        It will be called for every widget that has an after_editing function defined, 
        even if it is not visible on the screen. The after_editing function should return 
        True to indicate that editing of this form can continue, or False to indicate that 
        editing of this form should stop.
        """

        self.value = None
        self.wg_note_name.value = None
        self.wg_note.value = ""

        self.parentApp.getForm('ADD NOTE').name = "Add note"

    def data_validation(self) -> bool:
        """
        The data_validation function is used to validate the data entered by the user.
        It checks if the note is empty and if it contains only letters, numbers or spaces.
        If not, an error message will be displayed.
        """

        note = self.wg_note.value
        message_error = note_validation(note)
        if message_error:
            npyscreen.notify_confirm(message_error, "Error", editw=1)
            self.wg_note.value = ""
            return False
        return True

    def add_note(self) -> str:
        """
        The add_note function adds a note to the notesbook.
        It takes in a self parameter, which is an instance of the AddNoteForm class.
        The function returns a string that says &quot;The note has been added&quot; if it was successful.
        """

        note = Note(self.wg_note.value)
        record_note = RecordNote(note)

        if self.wg_note_name.value:
            record_note.add_note_name(self.wg_note_name.value)

        self.parentApp.notesbook.add_record(record_note)
        self.parentApp.notesbook.save_records_to_file(FILE_NB)
        return "The note has been added"

    def change_note(self) -> str:
        """
        The change_note function is used to change a note in the notesbook.
        It takes as input self, which is an instance of the ChangeNoteForm class.
        The function deletes the record that was selected by the user from 
        self.parentApp.notesbook and then calls add_note() to create a new record with 
        updated information.
        """

        self.parentApp.notesbook.delete_record(self.value)
        message = self.add_note()
        message = "The note has been updated"
        return message

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses OK.
        It checks if the data entered by the user is valid, and then either adds a new note or changes an existing one.
        If it's successful, it displays a message to confirm that the note has been saved.
        """

        if self.data_validation():
            if not self.value:
                message = self.add_note()
                self.after_editing()
                npyscreen.notify_confirm(message, "Saved!", editw=1)

            else:
                message = self.change_note()
                self.after_editing()
                npyscreen.notify_confirm(message, "Saved!", editw=1)

            self.parentApp.switchForm("NOTE MAIN")

    def on_cancel(self) -> None:
        """
        The on_cancel function is called when the user presses the cancel button.
        It will return to the previous form, which in this case is NOTE MAIN.
        """

        self.after_editing()
        self.parentApp.switchForm("NOTE MAIN")
