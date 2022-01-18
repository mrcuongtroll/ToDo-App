from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import datetime
import calendar
import data


# Constants:
SIGN_UP = 'sign up'
ADD_USER = 'add user'
VIEW_USER = 'view_user'
DAYS_31 = tuple(range(1, 32))
DAYS_30 = tuple(range(1, 31))
DAYS_29 = tuple(range(1, 30))
DAYS_28 = tuple(range(1, 29))
MONTHS_FULL = tuple(calendar.month_name[i] for i in range(1, 13))
MONTHS_SHORT = tuple(calendar.month_abbr[i] for i in range(1, 13))
YEARS_PAST = tuple(range(datetime.datetime.now().year-100, datetime.datetime.now().year+1))
YEARS_FUTURE = tuple(range(datetime.datetime.now().year, datetime.datetime.now().year+100))


# Classes
class _InfoFrame(ttk.Frame):

    def __init__(self, master=None, editable=True, acc_info: dict = None):
        super().__init__(master)
        self.master = master
        self.acc_info = acc_info

        # Name
        self.name_frame = ttk.Frame(self, padding=8)
        self.name_frame.pack(anchor=W, fill=X)
        self.first_name = ttk.Label(self.name_frame, text='First name', padding=5)
        self.first_name.grid(row=0, column=0, sticky=W)
        self.first_name_entry = ttk.Entry(self.name_frame)
        self.first_name_entry.grid(row=0, column=1, sticky=W)
        self.last_name = ttk.Label(self.name_frame, text='Last name', padding=5)
        self.last_name.grid(row=0, column=2, sticky=E)
        self.last_name_entry = ttk.Entry(self.name_frame)
        self.last_name_entry.grid(row=0, column=3, sticky=E)
        # Date of birth
        self.dob_frame = ttk.Frame(self, padding=8)
        self.dob_frame.pack(anchor=W, fill=X)
        self.year_label = ttk.Label(self.dob_frame, text='Year', padding=5)
        self.year_label.grid(row=0, column=0)
        self.year_option = ttk.Combobox(self.dob_frame, values=YEARS_PAST, width=5)
        self.year_option.grid(row=0, column=1)
        self.year_option.bind('<<ComboboxSelected>>', self.enumerate_days)
        self.month_label = ttk.Label(self.dob_frame, text='Month', padding=5)
        self.month_label.grid(row=0, column=2)
        self.month_option = ttk.Combobox(self.dob_frame, values=MONTHS_FULL, width=10)
        self.month_option.grid(row=0, column=3)
        self.month_option.bind('<<ComboboxSelected>>', self.enumerate_days)
        self.day_label = ttk.Label(self.dob_frame, text='Day', padding=5)
        self.day_label.grid(row=0, column=4)
        self.day_option = ttk.Combobox(self.dob_frame, values=DAYS_31, width=5)
        self.day_option.grid(row=0, column=5)
        # Address
        self.address_frame = ttk.Frame(self, padding=8)
        self.address_frame.pack(anchor=W, fill=X)
        self.address_label = ttk.Label(self.address_frame, text='Address', padding=5)
        self.address_label.grid(row=0, column=0, sticky=W)
        self.address_entry = ttk.Entry(self.address_frame, width=90)
        self.address_entry.grid(row=0, column=1, sticky=E+W)

        # Add account info if provided
        if acc_info is not None:
            self.view_info()

        # Configures
        self.set_editable(editable)

    def enumerate_days(self, event=None):
        try:
            year = int(self.year_option.get())
        except ValueError:
            year = datetime.datetime.now().year
        try:
            month = MONTHS_FULL.index(self.month_option.get()) + 1
            num_days = calendar.monthrange(year, month)[1]
            days = [day for day in range(1, num_days+1)]
            self.day_option['values'] = days
            if self.day_option.get() != '':
                if int(self.day_option.get()) > max(days):
                    self.day_option.delete(0, END)
                    self.day_option.insert(0, max(days))
        except ValueError:
            self.day_option['values'] = list(range(1, 32))
        return

    def set_editable(self, editable=True):
        if editable:
            state = NORMAL
        else:
            state = DISABLED
        self.first_name_entry.config(state=state)
        self.last_name_entry.config(state=state)
        self.year_option.config(state=state)
        self.month_option.config(state=state)
        self.day_option.config(state=state)
        self.address_entry.config(state=state)

    def update_info(self):
        if self.acc_info:
            self.acc_info['first_name'] = self.first_name_entry.get()
            self.acc_info['last_name'] = self.last_name_entry.get()
            self.acc_info['birth_year'] = self.year_option.get()
            self.acc_info['birth_month'] = self.month_option.get()
            self.acc_info['birth_day'] = self.day_option.get()
            self.acc_info['address'] = self.address_entry.get()

    def view_info(self):
        self.first_name_entry.insert(0,
                                     '' if not self.acc_info['first_name'] else self.acc_info['first_name'])
        self.last_name_entry.insert(0,
                                    '' if not self.acc_info['last_name'] else self.acc_info['last_name'])
        self.year_option.insert(0,
                                '' if not self.acc_info['birth_year'] else self.acc_info['birth_year'])
        self.month_option.insert(0,
                                 '' if not self.acc_info['birth_month'] else self.acc_info['birth_month'])
        self.day_option.insert(0,
                               '' if not self.acc_info['birth_day'] else self.acc_info['birth_day'])
        self.address_entry.insert(0,
                                  '' if not self.acc_info['address'] else self.acc_info['address'])
        return


class _UserFormWindow(Toplevel):

    def __init__(self, master=None, accounts_data: dict = None, mode='sign up', deiconify_master=True,
                 username=None):
        super().__init__()
        self.master = master
        self.accounts = accounts_data
        self.mode = mode
        self.deiconify_master = deiconify_master
        self.username = username

        # Basic setups
        if self.mode == SIGN_UP:
            self.title('ToDo List - Sign up')
        elif self.mode == ADD_USER:
            self.title('ToDo List - Add user')
        elif self.mode == VIEW_USER:
            assert self.username is not None, "Username must be provided in User's details form"
            self.title('ToDo List - User details')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'640x480+{int(screen_width / 2 - 320)}+{int(screen_height / 2 - 240)}')
        self.resizable(False, False)
        self.style = ttk.Style(self)

        # The title
        self.label_frame = ttk.Frame(self, relief=FLAT, padding=20)
        self.label_frame.pack()
        if self.mode == SIGN_UP:
            self.label = ttk.Label(self.label_frame, text='Sign up', style='FormTitle.TLabel')
        elif self.mode == ADD_USER:
            self.label = ttk.Label(self.label_frame, text='Add user account', style='FormTitle.TLabel')
        elif self.mode == VIEW_USER:
            self.label = ttk.Label(self.label_frame, text="User's details", style='FormTitle.TLabel')
        self.label.pack()

        # The information form
        self.main_frame = ttk.Frame(self, relief=GROOVE, padding=5)
        self.main_frame.pack(fill=BOTH)
        # Mandatory information: username and password
        if self.mode != VIEW_USER:
            self.mandatory_frame = ttk.LabelFrame(self.main_frame, text='Required information', padding=10)
        else:
            self.mandatory_frame = ttk.LabelFrame(self.main_frame, text='Account', padding=10)
        self.mandatory_frame.pack(fill=X)
        self.username_label = ttk.Label(self.mandatory_frame, text='Username', padding=5)
        self.username_label.grid(row=0, column=0, sticky=W)
        self.username_entry = ttk.Entry(self.mandatory_frame, width=30)
        self.username_entry.grid(row=0, column=1, sticky=W)
        self.password_label = ttk.Label(self.mandatory_frame, text='Password', padding=5)
        self.password_label.grid(row=1, column=0, sticky=W)
        self.password_entry = ttk.Entry(self.mandatory_frame, show='*', width=30)
        self.password_entry.grid(row=1, column=1, sticky=W)
        if self.mode != VIEW_USER:
            self.confirm_password_label = ttk.Label(self.mandatory_frame, text='Confirm password', padding=5)
            self.confirm_password_label.grid(row=2, column=0, sticky=W)
            self.confirm_password_entry = ttk.Entry(self.mandatory_frame, show='*', width=30)
            self.confirm_password_entry.grid(row=2, column=1, sticky=E)
        else:
            self.restriction_frame = ttk.LabelFrame(self.mandatory_frame, text='Restriction', padding=2)
            self.restriction_frame.grid(row=0, column=2, rowspan=2, sticky=N+S+E)
            self.mandatory_frame.columnconfigure(index=1, weight=1)
            self.date_entry = tkcalendar.DateEntry(self.restriction_frame)
            self.date_entry.grid(row=0, column=0, columnspan=2)
            self.restrict_button = ttk.Button(self.restriction_frame,
                                              text='Restrict user',
                                              width=20,
                                              command=self.restrict_user)
            self.restrict_button.grid(row=1, column=0)
            self.restrict_remove_button = ttk.Button(self.restriction_frame,
                                                     text='Remove restriction',
                                                     width=20,
                                                     command=self.remove_restriction)
            self.restrict_remove_button.grid(row=1, column=1)
        # Optional information: Name, date of birth
        if self.mode != VIEW_USER:
            self.optional_frame = ttk.LabelFrame(self.main_frame,
                                                 text='Optional information (You can update these information later)',
                                                 padding=2)
            self.info_frame = create_info_frame(self.optional_frame)
        else:
            self.optional_frame = ttk.LabelFrame(self.main_frame,
                                                 text='Information',
                                                 padding=2)
            self.info_frame = create_info_frame(self.optional_frame,
                                                editable=False,
                                                acc_info=self.accounts['accounts'][self.username])
        self.optional_frame.pack(fill=X)
        self.info_frame.pack()

        # The buttons
        self.button_frame = ttk.Frame(self, relief=FLAT, padding=20)
        self.button_frame.pack()
        if self.mode == SIGN_UP:
            self.login_now = IntVar(self)
            self.login_checkbox = ttk.Checkbutton(self.button_frame,
                                                  text='Log in now',
                                                  padding=5,
                                                  variable=self.login_now)
            self.login_checkbox.pack()
            self.login_checkbox.state(['!alternate'])
            self.signup_button = ttk.Button(self.button_frame, text='Sign up', command=self.signup)
            self.signup_button.pack()
        elif self.mode == ADD_USER:
            self.add_user_button = ttk.Button(self.button_frame, text='Add user', command=self.add_user)
            self.add_user_button.pack()
        elif self.mode == VIEW_USER:
            self.edit_button = ttk.Button(self.button_frame,
                                          text='Edit',
                                          width=10,
                                          command=self.edit_user)
            self.edit_button.grid(row=0, column=0, sticky=W)
            self.save_button = ttk.Button(self.button_frame,
                                          text='Save',
                                          width=10,
                                          command=self.update_user_info)
            self.save_button.grid(row=0, column=1, sticky=W)
            self.cancel_button = ttk.Button(self.button_frame,
                                            text='Cancel',
                                            width=10,
                                            command=self.destroy)
            self.cancel_button.grid(row=1, column=0, columnspan=2)

        # Style and theme
        self.style.configure('FormTitle.TLabel', font='Calibri 30')

        # View mode:
        if self.mode == VIEW_USER:
            self.view_mode()

    def destroy(self):
        if self.deiconify_master:
            self.master.deiconify()
        super().destroy()
        return

    def signup(self, event=None):
        if not self.username_entry.get() or not self.password_entry.get():
            messagebox.showerror('Error', 'Your username and password are required')
            self.lift()     # Bring the form to the front of the screen
        elif self.username_entry.get() in self.accounts['accounts'].keys():
            messagebox.showerror('Error', 'Username already exists')
            self.lift()
        elif not self.confirm_password_entry.get():
            messagebox.showerror('Error', 'Please confirm your password')
            self.lift()
        elif self.confirm_password_entry.get() != self.password_entry.get():
            messagebox.showerror('Error', "Password confirmation doesn't match")
            self.lift()
        else:
            username = self.username_entry.get()
            password = self.password_entry.get()
            role = 'user'
            first_name = self.info_frame.first_name_entry.get() if self.info_frame.first_name_entry.get() else None
            last_name = self.info_frame.last_name_entry.get() if self.info_frame.last_name_entry.get() else None
            if not self.info_frame.year_option.get():
                birth_year = None
            elif self.info_frame.year_option.get() not in self.info_frame.year_option['values']:
                return messagebox.showerror('Error', 'Invalid year')
            else:
                birth_year = self.info_frame.year_option.get()
            if not self.info_frame.month_option.get():
                birth_month = None
            elif self.info_frame.month_option.get() not in self.info_frame.month_option['values']:
                return messagebox.showerror('Error', 'Invalid month')
            else:
                birth_month = self.info_frame.month_option.get()
            if not self.info_frame.day_option.get():
                birth_day = None
            elif self.info_frame.day_option.get() not in self.info_frame.day_option['values']:
                return messagebox.showerror('Error', 'Invalid day')
            else:
                birth_day = self.info_frame.day_option.get()
            address = self.info_frame.address_entry.get() if self.info_frame.address_entry.get() else None
            new_account = data.Account(password=password,
                                       role=role,
                                       first_name=first_name,
                                       last_name=last_name,
                                       birth_year=birth_year,
                                       birth_month=birth_month,
                                       birth_day=birth_day,
                                       address=address)
            self.accounts['accounts'][username] = new_account.to_dict()
            messagebox.showinfo('Success', 'Account created successfully')
            self.destroy()
            if self.mode == 'sign up':
                if self.login_now.get():
                    self.master.login(username, password)
        return

    def add_user(self, event=None):
        self.signup()
        return

    def view_mode(self, event=None):
        assert self.mode == VIEW_USER, "View mode can only be accessed in VIEW_USER mode"
        # Show info
        self.username_entry.insert(0, self.username)
        self.password_entry.insert(0, self.accounts['accounts'][self.username]['password'])
        restriction = self.accounts['accounts'][self.username]['restriction']
        if restriction is not None and restriction != 'indefinite':
            restriction = datetime.datetime.strptime(restriction, '%m/%d/%Y')
            self.date_entry.set_date(restriction)
        # Disable everything
        self.username_entry.config(state=DISABLED)
        self.password_entry.config(state=DISABLED, show='*')
        self.info_frame.set_editable(False)
        self.date_entry.config(state=DISABLED)
        self.restrict_button.config(state=DISABLED)
        self.restrict_remove_button.config(state=DISABLED)
        self.save_button.config(state=DISABLED)
        self.edit_button.config(state=NORMAL)
        return

    def edit_user(self, event=None):
        confirm_password = input_string_dialog(self, 'Confirm password', 'Confirm admin password', show='*')
        if confirm_password == self.accounts['accounts']['admin']['password']:
            # Show everything
            self.password_entry.config(state=NORMAL, show='')
            self.info_frame.set_editable(True)
            restriction = self.accounts['accounts'][self.username]['restriction']
            if restriction is None:
                self.date_entry.config(state=NORMAL)
                self.restrict_button.config(state=NORMAL)
            else:
                self.restrict_remove_button.config(state=NORMAL)
            self.save_button.config(state=NORMAL)
            self.edit_button.config(state=DISABLED)
        else:
            messagebox.showerror('Error', "Your password confirmation doesn't match")
            self.lift()
        return

    def update_user_info(self, event=None):
        # Update info
        self.info_frame.update_info()
        self.accounts['accounts'][self.username]['password'] = self.password_entry.get()
        # Re-hide everything
        self.view_mode()
        return

    def restrict_user(self, event=None):
        restriction = self.date_entry.get_date()
        restriction = restriction.strftime('%m/%d/%Y')
        self.accounts['accounts'][self.username]['restriction'] = restriction
        self.date_entry.config(state=DISABLED)
        self.restrict_button.config(state=DISABLED)
        self.restrict_remove_button.config(state=NORMAL)
        return

    def remove_restriction(self, event=None):
        self.accounts['accounts'][self.username]['restriction'] = None
        self.date_entry.config(state=NORMAL)
        self.restrict_remove_button.config(state=DISABLED)
        self.restrict_button.config(state=NORMAL)
        return


class _InputDialog(Toplevel):

    def __init__(self, master=None, title='', prompt='', show=None):
        super().__init__()
        self.master = master
        self.style = ttk.Style(self)
        self.title(title)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'250x100+{int(screen_width / 2 - 125)}+{int(screen_height / 2 - 50)}')
        self.resizable(False, False)

        self.frame = ttk.Frame(self, relief=FLAT, padding=15)
        self.frame.pack()
        self.prompt = ttk.Label(self.frame, text=prompt)
        self.prompt.grid(row=0, column=0, columnspan=2, sticky=N)
        self.text = StringVar(self)
        self.text.trace_add('write', callback=lambda arg1, arg2, arg3: self.trace_entry())
        if show == '*':
            self.entry = ttk.Entry(self.frame, show='*', textvariable=self.text, width=30, exportselection=0)
        else:
            self.entry = ttk.Entry(self.frame, textvariable=self.text, width=30, exportselection=0)
        self.entry.grid(row=1, column=0, columnspan=2)
        self.entry.bind('<Return>', self.ok_button_pressed)
        self.ok_button = ttk.Button(self.frame, text='OK', state=DISABLED, command=self.ok_button_pressed)
        self.ok_button.grid(row=2, column=0, stick=S+E)
        self.cancel_button = ttk.Button(self.frame, text='Cancel', command=self.cancel_button_pressed)
        self.cancel_button.grid(row=2, column=1, sticky=S+W)

        self.entry.focus_force()
        self.wait_window()

    def trace_entry(self):
        try:
            if self.entry.get():
                self.ok_button.config(state=NORMAL)
            else:
                self.ok_button.config(state=DISABLED)
        except:
            return

    def destroy(self):
        # If you quit this dialog window then nothing will be returned
        self.text.set('')
        super().destroy()

    def ok_button_pressed(self, event=None):
        # If quit using the ok button then the content in the entry will be returned
        if self.text.get():
            super().destroy()
            return self.text.get()

    def cancel_button_pressed(self, event=None):
        self.destroy()


# Functions
def create_info_frame(master=None, editable=True, acc_info=None):
    return _InfoFrame(master, editable, acc_info)


def create_user_form(master=None, accounts_data=None, mode=SIGN_UP, deiconify_master=True, username=None):
    return _UserFormWindow(master, accounts_data, mode, deiconify_master, username)


def input_string_dialog(master=None, title='', prompt='', show='*'):
    dialog = _InputDialog(master, title, prompt, show)
    return dialog.text.get()


def style_map(widget, **kwargs):
    for attr, value in kwargs.items():
        widget[attr] = value
