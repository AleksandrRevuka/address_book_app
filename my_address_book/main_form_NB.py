import npyscreen

from my_address_book.interface_main_form import MainForm
from my_address_book.notes_book import NotesBook as NB
from my_address_book.utils import print_all_notes


class MainFormNB(MainForm):
    """
    MainForm is the main form of the address book application.

    This form displays the list of contacts, allows searching for contacts,
    and provides menu options for adding, editing, and deleting contacts.

    Methods:
        while_editing: Called when editing the search criteria, performs search and updates the contact list.
        search_contact:
        beforeEditing: Called before the form is displayed, updates the list of contacts.
        update_list: Updates the list of contacts in the address book to reflect any changes.
    """

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """

        self.print_widget = self.add(npyscreen.TitlePager, name="Notes:   ", begin_entry_at=9, max_height=36)
        self.search_widget = self.add(npyscreen.TitleText, name="Search:", rely=39, begin_entry_at=10)
        self.search_widget.when_cursor_moved = self.while_editing

        self.menu = self.new_menu(name="Menu")
        self.menu.addItem("Add note", self.add_note, "1")
        self.menu.addItem("Edit note", self.edit_note, "2")
        self.menu.addItem("Delete note", self.delete_note, "3")
        self.menu.addItem("Addressbook", self.to_addressbook_form, "4")
        self.menu.addItem("Sorting files", self.to_sorting_files_fotm, "5")
        self.menu.addItem("Close Menu", self.close_menu, "^X")
        self.menu.addItem("Exit", self.exit, "^E")

    def while_editing(self, *args: list, **kwargs: dict) -> None:
        """
        The while_editing function is a function that is called every time the user presses a key while editing
        the widget. It takes two arguments: self and *args, **kwargs. The self argument refers to the widget itself,
        and args/kwargs are arguments passed in by npyscreen when it calls this function (they're not used here).
        This function searches for notes that match what's currently in the search box.
        """

        notesbook: NB = self.parentApp.notesbook
        self.search_note(notesbook)

    def search_note(self, notesbook: NB) -> None:
        """
        The search_note function is used to search for notes in the NotesBook.
        It takes two arguments: self and notesbook.
        The first argument, self, is a reference to the current form object (SearchForm).
        The second argument, notesbook, is a reference to an instance of NotesBook class.
        This function uses criteria_validation function from criteria_validation module
        to validate user input before searching for it in the NotesBook instance.
        """

        if self.search_widget.value:
            criteria = self.search_widget.value
            searched_notes = notesbook.search(criteria)
            self.update_list(searched_notes)
        else:
            self.update_list(notesbook)

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data from your application.
        """

        notessbook = self.parentApp.notesbook
        self.update_list(notessbook)

    def update_list(self, notessbook: NB) -> None:
        """
        The update_list function is used to update the list of notes in the main form.
        It takes a NotesBook object as an argument and returns None. It updates the values
        of self.print_widget, which is a MultiLineEdit widget that displays all of the
        notes in notessbook.
        """

        contacts = print_all_notes(notessbook)
        self.print_widget.values = contacts.split("\n")
        self.print_widget.display()

    def add_note(self) -> None:
        """
        The add_note function is called when the user presses the &quot;Add Note&quot; button on
        the MainForm. It switches to a new form, AddNoteForm, which allows the user to
        enter information about a note they want to add.
        """

        self.parentApp.switchForm("ADD NOTE")

    def edit_note(self) -> None:
        """
        The edit_note function is called when the user presses the 'e' key while on a note.
        It switches to the EDIT NOTE form, which allows users to edit their notes.
        """

        self.parentApp.switchForm("EDIT NOTE")

    def delete_note(self) -> None:
        """
        The delete_note function is called when the user presses the delete note button on
        the main form. It switches to a new form, which allows the user to select a note from
        a list of all notes in their notebook and then deletes it.
        """
        self.parentApp.switchForm("DELETE NOTE")

    def to_addressbook_form(self) -> None:
        """
        The addressbook_form function is the main function of the addressbook_form module.
        It creates a form that allows users to add, edit, and delete entries in their address book.
        The form also has a search feature that allows users to find entries based on criteria they specify.
        """
        self.parentApp.switchForm("MAIN")

    def to_sorting_files_fotm(self) -> None:
        """
        The to_sorting_files_fotm function is a callback function that switches the current form to the SORT MAIN form.
        """
        self.parentApp.switchForm("SORT MAIN")
