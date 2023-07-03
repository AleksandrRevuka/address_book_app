from pathlib import Path
import os
import npyscreen

from my_address_book.sorting_files import SortingFiles
from my_address_book.interface_main_form import MainForm
from my_address_book.validation import check_path_address_to_sort_files_in_it
from my_address_book.sort import main


class MainFormSF(MainForm):
    """..."""

    def __init__(self, **keywords):
        super().__init__(**keywords)
        self.structure = False

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """
        self.tree_display_name: npyscreen.TitleFixedText = self.add(npyscreen.TitleFixedText, name="Structure:", editable=False)
        self.tree_display: npyscreen.MLTreeAction = self.add(
            npyscreen.MLTreeAction, max_height=-1, ignore_root=False, relx=9, selectable=True
        )

        self.search_widget: npyscreen.TitleFilename = self.add(npyscreen.TitleFilename, name="Sort folder:", begin_entry_at=15)

        self.search_widget.when_value_edited = self.while_editing

        self.menu = self.new_menu(name="Menu")
        self.menu.addItem("Folder data", self.make_data, "1")
        self.menu.addItem("Folder structure", self.make_structure, "2")
        self.menu.addItem("Folder sort", self.sorting_files, "3")
        self.menu.addItem("Addressbook", self.to_addressbook_form, "4")
        self.menu.addItem("Notesbook", self.to_notesbook_form, "5")
        self.menu.addItem("Folder sort", self.sorting_files_, "6")
        self.menu.addItem("Close Menu", self.close_menu, "^X")
        self.menu.addItem("Exit", self.exit, "^E")

    def beforeEditing(self) -> None:
        home_dir = str(Path.home())
        tree_start_data = npyscreen.TreeData()
        self.make_folder_data(home_dir, tree_start_data)
        self._update_widget(tree_start_data)
        self.search_widget.value = home_dir

    def while_editing(self, *args: list, **kwargs: dict) -> None:
        self.search_folder()

    def search_folder(self):
        if self.search_widget.value:
            if os.path.isdir(self.search_widget.value):
                if self.structure:
                    self.make_structure()
                else:
                    self.make_data()

    def to_notesbook_form(self) -> None:
        """
        The to_notesbook_fotm function is a callback function that switches the current form to the NOTE MAIN form.
        It takes in one parameter, self, which is an instance of AddressBookForm. It returns None.
        """
        self.parentApp.switchForm("NOTE MAIN")

    def to_addressbook_form(self) -> None:
        """
        The addressbook_form function is the main function of the addressbook_form module.
        It creates a form that allows users to add, edit, and delete entries in their address book.
        The form also has a search feature that allows users to find entries based on criteria they specify.
        """
        self.parentApp.switchForm("MAIN")

    def _update_widget(self, tree_data: npyscreen.TreeData) -> None:
        self.tree_display.values = tree_data
        self.tree_display.display()

    def make_data(self) -> None:
        directory = self.search_widget.value
        tree_new_data = npyscreen.TreeData()
        self.structure = False
        self.make_folder_data(directory, tree_new_data)
        self._update_widget(tree_new_data)

    def make_structure(self) -> None:
        directory = self.search_widget.value
        tree_new_data = npyscreen.TreeData()
        self.structure = True
        npyscreen.notify_wait("Please wait loading data...", title="Wait!")
        self.make_folder_data(directory, tree_new_data)

        self._update_widget(tree_new_data)

    def make_folder_data(self, directory: str, parent: npyscreen.TreeData) -> None:
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)

            if os.path.isdir(full_path) and self.structure:
                node = parent.new_child(content=filename)
                self.make_folder_data(full_path, node)

            elif os.path.isdir(full_path) and not self.structure:
                parent.new_child(content=filename)

            else:
                parent.new_child(content=filename)

    def sorting_files(self) -> None:
        directory = self.search_widget.value
        path = Path(directory)
        message = check_path_address_to_sort_files_in_it(path)
        if message:
            npyscreen.notify_confirm(message, "Error", editw=1)
        else:
            main(directory)
            if self.structure:
                self.make_structure()
            else:
                self.make_data()
            message = f"Directory {directory} has been sorted successfully!"
            npyscreen.notify_confirm(message, "Successfully", editw=1)

    def sorting_files_(self) -> None:
        directory = self.search_widget.value
        path = Path(directory)
        message = check_path_address_to_sort_files_in_it(path)
        if message:
            npyscreen.notify_confirm(message, "Error", editw=1)
        else:
            sorting_files = SortingFiles(path)
            sorting_files.files_addresses()
            sorting_files.sort_extensions()
            sorting_files.removing_files()
            sorting_files.del_empty_folders()
            if self.structure:
                self.make_structure()
            else:
                self.make_data()
            message = f"Directory {directory} has been sorted successfully!"
            npyscreen.notify_confirm(message, "Successfully", editw=1)
