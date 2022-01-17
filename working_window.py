from tkinter import *
from tkinter import ttk
import os
import utils
import profile
import accounts_manager
import todo_list


# Classes
class _WorkingWindow(Tk):

    def __init__(self, mode='user'):
        super().__init__()
        self.mode = mode
        self.data_path = os.path.join(os.getcwd(), 'data/')

        # root window.
        self.title('ToDo List')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'640x480+{int(screen_width / 2 - 320)}+{int(screen_height / 2 - 240)}')
        # We need a ttk.Style object to manage the style of widgets
        self.style = ttk.Style(self)

        # Menu: including menus
        self.menu = Menu(self, tearoff=False)
        self.config(menu=self.menu)
        # File menu: contains options like logout, exit
        self.file_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Refresh', command=None)   # TODO: this
        self.file_menu.add_command(label='Log out', command=None)   # TODO: this
        self.file_menu.add_command(label='Exit', command=None)  # TODO: this
        # TODO: add more stuff here
        # Edit menu:
        self.edit_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Edit', menu=self.edit_menu)
        # TODO: add more stuff here

        # Notebook to switch between frames:
        self.notebook = ttk.Notebook(self, padding=5)
        self.notebook.pack(expand=True, side=LEFT, fill=BOTH, anchor=N+W)
        self.notebook.enable_traversal()    # (Shift) + Ctrl + Tab
        # To do list (The "main" working frame)
        self.todo_frame = todo_list.create_todo_frame(self.notebook)
        self.notebook.add(self.todo_frame, text='To do list')
        # Profile: The user can view their profile info here
        self.profile_frame = profile.create_profile_frame(self.notebook)
        self.notebook.add(self.profile_frame, text='Your profile')
        # Accounts manager: For the admin to manage user accounts
        if self.mode == 'admin':
            self.accounts_manager_frame = accounts_manager.create_accounts_manager_frame(self.notebook)
            self.notebook.add(self.accounts_manager_frame, text='Manage user accounts')

        # main loop
        self.mainloop()


# Functions
def create_working_window(mode='user'):
    _WorkingWindow(mode=mode)
