"""
tkinter TO-DO list assignment
author: Hannah Andrade Lucki
"""


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import xml.etree.ElementTree as ET


class Application(tk.Tk):
    """
    Main Application class.
    Inherits from tkinter.Tk, which means it has all
    the attributes and behaviour its superclass has.
    """

    def __init__(self):
        """
        Initialiser of the Application class.
        It is invoked after the root window object is constructed/instantiated.
        """
        super().__init__() # invoking superclass' (tkinter.Tk) __init__ method
        self.resizable(width=False, height=False) # forbidding resizing the app
        self.title('Todo') # setting the app's title in the titlebar

        # instantiating tkinter's variable class and attaching the
        # callback method to be invoked whenever the variable is written

        self._search_var = tk.StringVar()
        self._search_var.trace_add('write', self._autosearch)
        self._create_widgets() # instantiating graphical user interface
        self.notes = [] # instantiating main data structure to keep notes
        self._load_notes() # loading notes from the .XML file into the treeview

    def _create_widgets(self):
        """
        Instantiating all the root window widgets while
        both configuring and laying them out properly.
        """

        # instantiating all frame widgets that
        # will act as containers for other widgets

        search_frame = tk.Frame(self)
        search_frame.grid(row=0, column=0, sticky='w')
        treeview_frame = tk.Frame(self)
        treeview_frame.grid(row=1, column=0, sticky='w')
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=2, column=0, sticky='w')

        # instantiating search entry for autosearch functionality

        self.search_entry = tk.Entry(search_frame, width=31, textvariable=self._search_var)
        self.search_entry.grid(row=0, column=0)

        # instantiating the main treeview display widget
        # and configuring its columns and headings

        self.treeview = ttk.Treeview(treeview_frame, height=12, columns=('Subject', 'Priority'))
        self.treeview.grid(row=0, column=0, sticky='we')
        self.treeview.column('#0', minwidth=0, width=35,stretch='no', anchor='w')
        self.treeview.heading('#0', text='#')
        self.treeview.column('Subject', minwidth=0, width=156, stretch='no', anchor='w')
        self.treeview.heading('Subject', text='Subject')
        self.treeview.column('Priority', minwidth=0, width=57,stretch='no', anchor='w')
        self.treeview.heading('Priority', text='Priority')

        # instantiating all the buttons

        add_button = tk.Button(buttons_frame, width=7, text='Add',command=self.add_item)
        add_button.grid(row=0, column=0)

        remove_button = tk.Button(buttons_frame, width=7, text='Remove',command=self.remove_item)
        remove_button.grid(row=0, column=1)

        edit_button = tk.Button(buttons_frame,width=7, text='Edit',command=self.edit_item)
        edit_button.grid(row=0, column=2)

    def on_closing(self):
        """
        Helper callback method that is invoked
        whenever the root window is closed.
        """
        self.save_all() # saving notes to XML file

        # prompt the user with a messagebox

        if messagebox.askokcancel('Quit', 'Are you sure you want to quit?'):
            # if 'ok' was clicked on the messagebox
            self.destroy() # close the window

    def _load_notes(self):
        """
        Loading notes from .xml file into the treeview
        """
        # clearing the treeview
        self.treeview.delete(*self.treeview.get_children())
        self.notes.clear() # clearing the data structure (list)
        path = os.getcwd() # get current working directory
        todo_path = os.path.join(path, 'Todo', 'Notes.xml') # XML file path
        if not os.path.exists(todo_path):
            # if the path to the XML file does not exist
            if not os.path.exists(os.path.dirname(todo_path)):
                # create the application directory
                # if it does not already exist
                os.mkdir(os.path.dirname(todo_path))
            doc = ET.Element('Notes') # creating main node
            tree = ET.ElementTree(doc) # creating the XML ElementTree
            tree.write(todo_path) # writing the ElementTree to the file
        else:
            # if the path to the XML file already exists
            # create the XML ElementTree from the XML file
            tree = ET.ElementTree(file=todo_path)
        # for each node in the tree
        for node in tree.findall('Note'):
            # extract id, subject and priority from the node
            # and instantiate a custom Note object
            note = Note(node.find('Id').text, node.find('Subject').text, node.find('Priority').text)
            # append note object to the data structure
            self.notes.append(note)
            # display the note in the treeview
            self.treeview.insert('', 'end',text=note.id,values=(note.subject, note.priority))

    def save_all(self):
        """
        Saving notes from the treeview into .xml file
        """
        path = os.getcwd() # get current working directory
        todo_path = os.path.join(path, 'Todo', 'Notes.xml') # XML file path
        tree = ET.ElementTree(file=todo_path) # creating XML ElementTree
        # for each node in the ElementTree
        for node in tree.getroot().findall('Note'):
            # removing the node
            tree.getroot().remove(node)
        # for each note in notes data structure
        for note in self.notes:
            # create top node
            top_node = ET.Element('Note')

            # dynamically creating the rest of the nodes
            # and configuring them appropriately

            for x in ['id', 'subject', 'priority']:
                exec('{0}_node = ET.Element("{1}")'.format(x, x.title()))
                exec('{0}_node.text = note.{0}'.format(x))
                exec('top_node.append({0}_node)'.format(x))
            # appending top (parent) node to the ElementTree
            tree.getroot().append(top_node)
        tree.write(todo_path) # writing changes to the XML file

    def add_item(self):
        """
        Helper method for adding item
        """
        dialog = DialogWindow(self, item_id=None) # instantiating dialog window
        dialog.wait_window() # invoking tkinter.Toplevel's event loop

    def remove_item(self):
        """
        Removing selected items from the treeview,
        as well as from our data structure in the same time.
        """

        # if there are selected items in the treeview
        if self.treeview.selection():
            # if 'yes' is clicked on the messagebox
            if messagebox.askyesno('Notification','Are you sure you want to remove selected items?'):
                # get selected items from the treeview
                selected_items = self.treeview.selection()
                # comparing each selected item's first value (subject)
                # with each note in our notes data structure
                for selected_item in selected_items:
                    # iterating over a copy of the list
                    # in order to prevent unexpected behaviour
                    # which happens with removing stuff from mutable objects
                    # while iterating over such
                    for note in self.notes[:]:
                        if note.subject == self.treeview.item(selected_item)['values'][0]:
                            # if there is a match, removing it from the list
                            self.notes.remove(note)
                    # removing selected item from the treeview
                    self.treeview.delete(selected_item)
        else:
            # display the messagebox if there are
            # no selected items in the treeview
            messagebox.showinfo('Notification','Make sure you have some items selected!')

    def edit_item(self):
        """
        Editing selected item
        """

        # if there is exactly only one selected item in the treeview
        if len(self.treeview.selection()) == 1:
            # if 'yes' is clicked on the messagebox
            if messagebox.askyesno('Notification','Are you sure you want to edit selected item?'):
                # getting selected item and its id from the treeview
                selected_item = self.treeview.selection()
                item_id = self.treeview.index(selected_item)
                # instantiating DialogWindow class and passing it the item_id
                dialog = DialogWindow(self, item_id=item_id)
                # invoke tkinter.Toplevel's event loop
                dialog.wait_window()
        else:
            # if there is less or more than one selected item in the treeview
            messagebox.showinfo('Notification','Make sure you have exactly one item selected!')

    def _autosearch(self, event):
        """
        Helper callback method for searching for notes, a part of tracing
        system we set up earlier. This method is automatically invoked
        whenever our search_var tkinter class variable is written.
        """

        # getting search string from the search entry widget
        search_string = self.search_entry.get().lower()

        # clearing the treeview (deleting all items in it)
        # in order to display only the search results
        self.treeview.delete(*self.treeview.get_children()) # unpacking

        # iterating over our notes data structure
        # in order to compare search string and each note's subject
        for note in self.notes:
            # standardising searching by lowercasing search string/note subject
            if search_string.lower() in note.subject.lower():
                # if there is a match, display it in the treeview widget
                self.treeview.insert('', 'end',text=note.id,values=(note.subject, note.priority))

    def find_note(self, note):
        """
        Helper method for finding the relevant note in the list
        """

        # for instance, the code below could be written as:
        #
        # for x in self._notes:
        #     if s.subject == note:
        #         return x
        #
        # ... but in this particular case I found the list comprehension
        # and indexing to be more readable, as well as far less to type.

        return [x for x in self.notes if x.subject == note][0]

class DialogWindow(tk.Toplevel):
    """
    DialogWindow class.
    Inherits from tkinter.Toplevel
    """

    def __init__(self, parent, item_id):
        """
        Initialiser of the DialogWindow class
        """
        super().__init__(parent) # invoking superclass' (tkinter.Toplevel) init
        # declaring instance variables
        self._parent = parent
        self._item_id = item_id
        self.resizable(width=False, height=False) # forbidding window resizing
        self._create_widgets() # creating graphical user interface

    def _create_widgets(self):
        """
        Instantiating all the dialog window widgets while
        both configuring and laying them out properly.
        """

        # instantiating all frame widgets that
        # will act as containers for other widgets

        text_frame = tk.Frame(self)
        text_frame.grid(row=0, column=0, sticky='w')

        combobox_frame = tk.Frame(self)
        combobox_frame.grid(row=1, column=0, sticky='w')

        helper_frame = tk.Frame(self)
        helper_frame.grid(row=2, column=0)

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=3, column=0)

        # instantiating widgets and descriptive labels to accompany them

        subject_label = tk.Label(text_frame, text='Subject:')
        subject_label.grid(row=0, column=0, sticky='w')

        self.subject_text = tk.Text(text_frame, width=28, height=9)
        self.subject_text.grid(row=1, column=0)

        priority_label = tk.Label(combobox_frame, text='Priority:')
        priority_label.grid(row=0, column=0, sticky='w')

        self.priority_combobox = ttk.Combobox(
            combobox_frame,
            width=17,
            values=('High', 'Medium', 'Low')
        )
        self.priority_combobox.grid(row=0, column=1)

        # instantiating buttons

        ok_button = tk.Button(
            buttons_frame,
            width=9, text='OK',
            command=self._adding_item
        )
        ok_button.grid(row=0, column=0)

        cancel_button = tk.Button(
            buttons_frame, width=9,
            text='Cancel',
            command=self._close_dialog
        )
        cancel_button.grid(row=0, column=1)

        #
        # MECHANISM BEHIND item_id:
        #
        # We actually need two windows, but there is only a small difference
        # between them, so in order to avoid writing such repetitive code, we
        # decided to design the DialogWindow class to accept item_id argument
        # when being instantiated.
        #
        # If item_id is None it means that no item_id was passed when
        # instantiating the dialog window, which in turn means that no item was
        # selected in the treeview and the dialog should open in 'add item' mode
        # as opposed to 'save item' mode needed when editing/saving the item.
        #

        if self._item_id is None:
            # configure ok button for 'add item' mode
            ok_button.configure(text='Ok', command=self._adding_item)
        else:
            # get subject & property for the selected item in the treeview
            selected_item = self._parent.treeview.selection()
            subject = self._parent.treeview.item(selected_item)['values'][0]
            priority = self._parent.treeview.item(selected_item)['values'][1]
            # clear subject text widget
            self.subject_text.delete('1.0', 'end')
            # clear priority combobox widget
            self.priority_combobox.delete(0, 'end')
            # inserting subject and priority into appropriate widgets
            self.subject_text.insert('end', subject)
            self.priority_combobox.insert(0, priority)
            # configure ok button for 'save item' mode
            ok_button.configure(text='Save', command=self.save_item)

    def _close_dialog(self):
        """
        Helper method for closing the dialog window
        """
        self.destroy()


    def _adding_item(self):
        """
        Adding item
        """
        if self.subject_text.get('1.0', 'end') and self.priority_combobox.get():
            # if both subject and priority were entered
            # set id to the number of items in the treeview
            i = len(self._parent.treeview.get_children())
            # instantiate a Note object
            note = Note(str(i),self.subject_text.get('1.0', 'end'),self.priority_combobox.get())
            # inserting the note into the treeview
            self._parent.treeview.insert('', 'end',text=note.id,values=(note.subject, note.priority))
            i += 1 # incrementing id
            self._parent.notes.append(note) # adding the note to the data structure
            self._close_dialog() # closing the dialog window
        else:
            # display the messagebox if either
            # subject or priority was not entered
            messagebox.showinfo('Notification','Please enter subject & priority!')

    def save_item(self):
        """
        Saving the edited item
        """

        # getting selected item vrom the treeview
        selected_item = self._parent.treeview.selection()
        # finding relevant note using our _find_note helper method
        note = self._parent.find_note(self._parent.treeview.item(selected_item)['values'][0])
        # configuring note's subject & priority
        note.subject = self.subject_text.get('1.0', '1.0 lineend')
        note.priority = self.priority_combobox.get()
        # deleting the selected item from the treeview
        self._parent.treeview.delete(selected_item)
        # inserting saved item in the treeview
        self._parent.treeview.insert('', 'end',text=note.id,values=(note.subject, note.priority))
        # closing the dialog window
        self._close_dialog()

class Note:
    """
    Helper class for representing custom Note objects
    """

    def __init__(self, _id, subject, priority):
        """
        Initialiser of the Note class
        It is invoked after the Note class is constructed/instantiated.
        """
        # declaring instance variables
        self.id = _id
        self.subject = subject
        self.priority = priority

def main():
    """
    Main function
    """
    # instantiating our main Application class
    app = Application()
    # attaching _on_closing callback method to DELETE_WINDOW protocol
    # which will be invoked whenever the user closes the application
    app.protocol('WM_DELETE_WINDOW', app.on_closing)
    # invoking the root window's mainloop
    app.mainloop()

if __name__ == '__main__':
    # Application's main entry point
    main()

