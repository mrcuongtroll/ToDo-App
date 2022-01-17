from tkinter import *
from tkinter import ttk
import os
import utils


# Classes
class _AccountsManagerFrame(ttk.Frame):

    def __init__(self, master=None):
        super().__init__()
        self.master = master

        # Control frame: Contains buttons and stuff
        self.control_frame = ttk.Frame(self, padding=30)
        self.control_frame.grid(row=0, column=0, sticky=N+S+E+W)
        self.add_button = ttk.Button(self.control_frame,
                                     text='Add new account',
                                     width=20,
                                     command=self.add_user)
        self.add_button.pack(pady=5)
        self.remove_button = ttk.Button(self.control_frame,
                                        text='Remove user',
                                        width=20,
                                        state=DISABLED,
                                        command=None)   # TODO: this
        self.remove_button.pack(pady=5)
        self.view_button = ttk.Button(self.control_frame,
                                      text='View details',
                                      width=20,
                                      state=DISABLED,
                                      command=None)     # TODO: this
        self.view_button.pack(pady=5)
        self.restrict_button = ttk.Button(self.control_frame,
                                          text='Restrict user',
                                          width=20,
                                          state=DISABLED,
                                          command=None)     # TODO: this
        self.restrict_button.pack(pady=5)

        # List frame: Contain user list
        self.list_frame = ttk.LabelFrame(self, text='User accounts', padding=2)
        self.list_frame.grid(row=0, column=1, sticky=N+S+E+W)
        self.list_frame.rowconfigure(index=0, weight=1)
        self.list_frame.columnconfigure(index=0, weight=1)
        self.accounts_list_xscrollbar = ttk.Scrollbar(self.list_frame, orient=HORIZONTAL)
        self.accounts_list_xscrollbar.grid(row=1, column=0, sticky=S+E+W)
        self.accounts_list_yscrollbar = ttk.Scrollbar(self.list_frame, orient=VERTICAL)
        self.accounts_list_yscrollbar.grid(row=0, column=1, sticky=N+S+E)
        self.accounts_list = ttk.Treeview(self.list_frame,
                                          selectmode=BROWSE,
                                          xscrollcommand=self.accounts_list_xscrollbar.set,
                                          yscrollcommand=self.accounts_list_yscrollbar.set)
        self.accounts_list.grid(row=0, column=0, sticky=N+S+E+W)
        self.accounts_list_xscrollbar.config(command=self.accounts_list.xview)
        self.accounts_list_yscrollbar.config(command=self.accounts_list.yview)
        self.accounts_list['columns'] = ('Username', 'Name', 'Date of birth', 'Address', 'Restriction')
        self.accounts_list.column('#0', width=0, minwidth=0, stretch=NO)
        for column in self.accounts_list['columns']:
            self.accounts_list.column(column, minwidth=100, anchor=W)
            self.accounts_list.heading(column, text=column)

        # Configures
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

    def add_user(self, event=None):
        utils.create_user_form(self, mode=utils.ADD_USER, deiconify_master=False)
        return


# Functions
def create_accounts_manager_frame(master=None):
    return _AccountsManagerFrame(master)
