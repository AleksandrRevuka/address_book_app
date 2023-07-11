from pathlib import Path
import os
import npyscreen

from my_address_book.interface_main_form import MainForm
from my_address_book.validation import check_path_address_to_sort_files_in_it
from my_address_book.garbage_sorter import sorter_run


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

        self.menu = self.new_menu(name="Menu")
        self.menu.addItem("Folder data", self.make_data, "1")
        self.menu.addItem("Folder structure", self.make_structure, "2")
        self.menu.addItem("Folder sort", self.sorting_files, "3")
        self.menu.addItem("Addressbook", self.to_addressbook_form, "4")
        self.menu.addItem("Notesbook", self.to_notesbook_form, "5")
        self.menu.addItem("Close Menu", self.close_menu, "^X")
        self.menu.addItem("Exit", self.exit, "^E")

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data.
        """
        home_dir = str(Path.home())
        tree_start_data = npyscreen.TreeData()
        self.make_folder_data(home_dir, tree_start_data)
        self._update_widget(tree_start_data)
        self.search_widget.value = home_dir

    def while_editing(self, *args: list, **kwargs: dict) -> None:
        """
        The while_editing function is a function that runs while the user is editing the field.
        It will be called every time the user presses a key, and it will be passed all of the arguments
        that were passed to add_handlers.  It can also accept keyword arguments.
        """
        self.search_folder()

    def search_folder(self):
        """
        The search_folder function is used to search for a folder in the system.
        It takes as an argument self, which is the current instance of the class.
        The function checks if there are any values in the search_widget and then checks if it's a directory or not.
        If it's a directory, then we check whether we want to make structure or data and call either one of them.
        """
        if self.search_widget.when_check_value_changed():
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
        """
        The _update_widget function is a helper function that updates the tree widget.
        It takes in a TreeData object and sets the values of the tree_display to be equal to it.
        Then, it calls display() on self.tree_display.
        """
        self.tree_display.values = tree_data
        self.tree_display.display()
        self.display()

    def make_data(self) -> None:
        """
        The make_data function is used to create the data that will be displayed in the tree widget.
        It takes a directory as an argument and then creates a TreeData object, which it populates with
        the contents of that directory. It then calls _update_widget to display this data.
        """
        directory = self.search_widget.value
        tree_new_data = npyscreen.TreeData()
        self.structure = False
        if os.path.isdir(directory):
            self.make_folder_data(directory, tree_new_data)
            self._update_widget(tree_new_data)

    def make_structure(self) -> None:
        """
        The make_structure function is used to create a tree structure of the directory that was entered by the user.
        The function takes in self as an argument and returns None. The function creates a variable called directory which
        is equal to the value of what was entered into the search widget (the text box where you enter your path). It then
        creates another variable called tree_new_data which is equal to npyscreen's TreeData() method, this allows us to use
        npyscreen's TreeData class methods on our new data set. We then set self.structure = True so we can access it later on
        """
        directory = self.search_widget.value
        tree_new_data = npyscreen.TreeData()
        self.structure = True
        npyscreen.notify_wait("Please wait loading data...", title="Wait!")
        if os.path.isdir(directory):
            self.make_folder_data(directory, tree_new_data)
            self._update_widget(tree_new_data)

    def make_folder_data(self, directory: str, parent: npyscreen.TreeData) -> None:
        """
        The make_folder_data function is used to create a tree structure of the files and folders in the directory.
        The function takes two arguments: self, which is an instance of TreeData class, and directory - a string that represents
        the path to the folder we want to display its content. The function returns None.
        """
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
        """
        The sorting_files function is used to sort files in a directory.
            Args:
                self (object): The object of the class MainForm.MainForm
        """
        directory = self.search_widget.value

        message = check_path_address_to_sort_files_in_it(directory)
        if message:
            npyscreen.notify_confirm(message, "Error", editw=1)
        else:
            message = sorter_run(directory)
            if self.structure:
                self.make_structure()
            else:
                self.make_data()
            if message:
                npyscreen.notify_confirm(message, "Error", editw=1)
            else:
                message = f"Directory {directory} has been sorted successfully!"
                npyscreen.notify_confirm(message, "Successfully", editw=1)
