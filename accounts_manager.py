from tkinter import *
from tkinter import ttk
import os
import utils


# Classes
class _AccountsManagerFrame(ttk.Frame):

    def __init__(self, master=None, accounts_data: dict = None):
        super().__init__()
        self.master = master
        self.accounts = accounts_data

        # Control frame: Contains buttons and stuff
        self.control_frame = ttk.Frame(self, padding=30)
        self.control_frame.grid(row=0, column=0, sticky=N+S+E+W)
        self.refresh_button = ttk.Button(self.control_frame,
                                         text='Refresh',
                                         width=20,
                                         command=self.refresh)
        self.refresh_button.pack(pady=5)
        self.add_button = ttk.Button(self.control_frame,
                                     text='Add new account',
                                     width=20,
                                     command=self.add_user)
        self.add_button.pack(pady=5)
        self.remove_button = ttk.Button(self.control_frame,
                                        text='Remove user',
                                        width=20,
                                        state=DISABLED,
                                        command=self.remove_user)
        self.remove_button.pack(pady=5)
        self.view_button = ttk.Button(self.control_frame,
                                      text='View details',
                                      width=20,
                                      state=DISABLED,
                                      command=self.view_user)
        self.view_button.pack(pady=5)
        self.restrict_button = ttk.Button(self.control_frame,
                                          text='Restrict user',
                                          width=20,
                                          state=DISABLED,
                                          command=self.restrict_user)
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
        # Bindings:
        self.accounts_list.bind('<Button-1>', self.click_out)
        self.accounts_list.tag_bind('user', '<Double-1>', self.view_user)
        self.accounts_list.tag_bind('user', '<Return>', self.view_user)
        self.accounts_list.tag_bind('user', '<Delete>', self.remove_user)
        self.accounts_list.tag_bind('user', '<<TreeviewSelect>>', self.account_select)

        # Configures
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        # First refresh
        self.refresh()

    def refresh(self, event=None):
        # First we clear the current list
        for acc in self.accounts_list.get_children():
            self.accounts_list.delete(acc)
        for username in self.accounts['accounts'].keys():
            # Don't display admin account
            if self.accounts['accounts'][username]['role'] == 'admin':
                continue
            first_name = '' if not self.accounts['accounts'][username]['first_name'] \
                else self.accounts['accounts'][username]['first_name']
            last_name = '' if not self.accounts['accounts'][username]['last_name'] \
                else self.accounts['accounts'][username]['last_name']
            name = f'{first_name} {last_name}'
            year = '' if not self.accounts['accounts'][username]['birth_year'] \
                else self.accounts['accounts'][username]['birth_year']
            try:
                month = '' if not self.accounts['accounts'][username]['birth_month'] \
                    else str(utils.MONTHS_FULL.index(self.accounts['accounts'][username]['birth_month'])+1)
            except ValueError:
                month = self.accounts['accounts'][username]['birth_month']
            day = '' if not self.accounts['accounts'][username]['birth_day'] \
                else self.accounts['accounts'][username]['birth_day']
            dob = f'{month}/{day}/{year}'
            address = '' if not self.accounts['accounts'][username]['address'] \
                else self.accounts['accounts'][username]['address']
            restriction = '' if not self.accounts['accounts'][username]['restriction'] \
                else self.accounts['accounts'][username]['restriction']
            self.accounts_list.insert(parent='',
                                      iid=username,
                                      tag=self.accounts['accounts'][username]['role'],
                                      index=END,
                                      values=(username, name, dob, address, restriction)
                                      )
        return

    def add_user(self, event=None):
        form = utils.create_user_form(self, accounts_data=self.accounts, mode=utils.ADD_USER, deiconify_master=False)
        self.wait_window(form)
        self.refresh()
        return

    def view_user(self, event=None):
        username = self.accounts_list.selection()[0]
        form = utils.create_user_form(self,
                                      accounts_data=self.accounts,
                                      mode=utils.VIEW_USER,
                                      deiconify_master=False,
                                      username=username
                                      )
        self.wait_window(form)
        self.refresh()
        return

    def remove_user(self, event=None):
        username = self.accounts_list.selection()[0]
        del self.accounts['accounts'][username]
        self.refresh()
        return

    def restrict_user(self, end_date=None, event=None):
        username = self.accounts_list.selection()[0]
        if end_date:
            self.accounts['accounts'][username]['restriction'] = end_date
        else:
            self.accounts['accounts'][username]['restriction'] = 'indefinite'
        self.refresh()
        return

    def account_select(self, event=None):
        if not self.accounts_list.selection():
            # If nothing is selected then disable some buttons
            self.reset_control()
        else:
            self.view_button.config(state=NORMAL)
            self.remove_button.config(state=NORMAL)
            self.restrict_button.config(state=NORMAL)
        return

    def reset_control(self, event=None):
        self.view_button.config(state=DISABLED)
        self.remove_button.config(state=DISABLED)
        self.restrict_button.config(state=DISABLED)
        return

    def click_out(self, event=None):
        # When the user click the space that contains no row
        if not self.accounts_list.identify_row(event.y):
            for acc in self.accounts_list.selection():
                self.accounts_list.selection_remove(acc)
        return


# Functions
def create_accounts_manager_frame(master=None, accounts_data=None):
    return _AccountsManagerFrame(master, accounts_data)
