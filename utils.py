from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import calendar
import data


# Classes
class _InfoFrame(ttk.Frame):

    def __init__(self, master=None, editable=True):
        super().__init__(master)
        self.master = master

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
        self.year_option = ttk.Combobox(self.dob_frame,
                                        values=YEARS_PAST,
                                        width=5)
        self.year_option.grid(row=0, column=1)
        self.year_option.bind('<<ComboboxSelected>>', self.enumerate_days)
        self.month_label = ttk.Label(self.dob_frame, text='Month', padding=5)
        self.month_label.grid(row=0, column=2)
        self.month_option = ttk.Combobox(self.dob_frame,
                                         values=MONTHS_FULL,
                                         width=10)
        self.month_option.grid(row=0, column=3)
        self.month_option.bind('<<ComboboxSelected>>', self.enumerate_days)
        self.day_label = ttk.Label(self.dob_frame, text='Day', padding=5)
        self.day_label.grid(row=0, column=4)
        self.day_option = ttk.Combobox(self.dob_frame,
                                       values=DAYS_31,
                                       width=5)
        self.day_option.grid(row=0, column=5)
        # Address
        self.address_frame = ttk.Frame(self, padding=8)
        self.address_frame.pack(anchor=W, fill=X)
        self.address_label = ttk.Label(self.address_frame, text='Address', padding=5)
        self.address_label.grid(row=0, column=0, sticky=W)
        self.address_entry = ttk.Entry(self.address_frame, width=90)
        self.address_entry.grid(row=0, column=1, sticky=E+W)

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


class _UserFormWindow(Tk):

    def __init__(self, master=None, accounts_data: dict = None, mode='sign up', deiconify_master=True):
        super().__init__()
        self.master = master
        self.accounts = accounts_data
        self.mode = mode
        self.deiconify_master = deiconify_master

        # Basic setups
        if self.mode == 'sign up':
            self.title('ToDo List - Sign up')
        else:
            self.title('ToDo List - Add user')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'640x480+{int(screen_width / 2 - 320)}+{int(screen_height / 2 - 240)}')
        self.resizable(False, False)
        self.style = ttk.Style(self)

        # The title
        self.label_frame = ttk.Frame(self, relief=FLAT, padding=20)
        self.label_frame.pack()
        if self.mode == 'sign up':
            self.label = ttk.Label(self.label_frame, text='Sign up', style='Title.TLabel')
        else:
            self.label = ttk.Label(self.label_frame, text='Add user account', style='Title.TLabel')
        self.label.pack()

        # The information form
        self.main_frame = ttk.Frame(self, relief=GROOVE, padding=5)
        self.main_frame.pack(fill=BOTH)
        # Mandatory information: username and password
        self.mandatory_frame = ttk.LabelFrame(self.main_frame, text='Required information', padding=10)
        self.mandatory_frame.pack(fill=X)
        self.username_label = ttk.Label(self.mandatory_frame, text='Username', padding=5)
        self.username_label.grid(row=0, column=0, sticky=W)
        self.username_entry = ttk.Entry(self.mandatory_frame, width=30)
        self.username_entry.grid(row=0, column=1, sticky=E)
        self.password_label = ttk.Label(self.mandatory_frame, text='Password', padding=5)
        self.password_label.grid(row=1, column=0, sticky=W)
        self.password_entry = ttk.Entry(self.mandatory_frame, show='*', width=30)
        self.password_entry.grid(row=1, column=1, sticky=E)
        self.confirm_password_label = ttk.Label(self.mandatory_frame, text='Confirm password', padding=5)
        self.confirm_password_label.grid(row=2, column=0, sticky=W)
        self.confirm_password_entry = ttk.Entry(self.mandatory_frame, show='*', width=30)
        self.confirm_password_entry.grid(row=2, column=1, sticky=E)
        # Optional information: Name, date of birth
        self.optional_frame = ttk.LabelFrame(self.main_frame,
                                             text='Optional information (You can update these information later)',
                                             padding=2)
        self.optional_frame.pack(fill=X)
        self.info_frame = create_info_frame(self.optional_frame)
        self.info_frame.pack()

        # The buttons
        self.button_frame = ttk.Frame(self, relief=FLAT, padding=20)
        self.button_frame.pack()
        if self.mode == 'sign up':
            self.login_now = IntVar(self)
            self.login_checkbox = ttk.Checkbutton(self.button_frame,
                                                  text='Log in now',
                                                  padding=5,
                                                  variable=self.login_now)
            self.login_checkbox.pack()
            self.login_checkbox.state(['!alternate'])
            self.signup_button = ttk.Button(self.button_frame, text='Sign up', command=self.signup)
            self.signup_button.pack()
        else:
            self.add_user_button = ttk.Button(self.button_frame, text='Add user', command=self.add_user)
            self.add_user_button.pack()

        # Style and theme
        self.style.configure('Title.TLabel', font='Calibri 30')

    def destroy(self):
        if self.deiconify_master:
            self.master.deiconify()
        super().destroy()
        return

    def signup(self, event=None):
        if not self.username_entry.get() or not self.password_entry.get():
            messagebox.showerror('Error', 'Your username and password are required')
        elif self.username_entry.get() in self.accounts['accounts'].keys():
            messagebox.showerror('Error', 'Username already exists')
        elif not self.confirm_password_entry.get():
            messagebox.showerror('Error', 'Please confirm your password')
        elif self.confirm_password_entry.get() != self.password_entry.get():
            messagebox.showerror('Error', "Password confirmation doesn't match")
        else:
            username = self.username_entry.get()
            password = self.password_entry.get()
            role = 'user'
            first_name = self.info_frame.first_name_entry.get() if self.info_frame.first_name_entry.get() else None
            last_name = self.info_frame.last_name_entry.get() if self.info_frame.last_name_entry.get() else None
            birth_year = self.info_frame.year_option.get() if self.info_frame.year_option.get() else None
            birth_month = self.info_frame.month_option.get() if self.info_frame.month_option.get() else None
            birth_day = self.info_frame.day_option.get() if self.info_frame.day_option.get() else None
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
            self.destroy()
            if self.mode == 'sign up':
                if self.login_now.get():
                    self.master.login(username, password)
        return

    def add_user(self, event=None):
        self.signup()
        return


# Functions
def create_info_frame(master=None, editable=True):
    return _InfoFrame(master, editable)


def create_user_form(master=None, accounts_data=None, mode='sign up', deiconify_master=True):
    return _UserFormWindow(master, accounts_data, mode, deiconify_master)


def style_map(widget, **kwargs):
    for attr, value in kwargs.items():
        widget[attr] = value


# Constants:
SIGN_UP = 'sign up'
ADD_USER = 'add user'
DAYS_31 = tuple(range(1, 32))
DAYS_30 = tuple(range(1, 31))
DAYS_29 = tuple(range(1, 30))
DAYS_28 = tuple(range(1, 29))
MONTHS_FULL = tuple(calendar.month_name[i] for i in range(1, 13))
MONTHS_SHORT = tuple(calendar.month_abbr[i] for i in range(1, 13))
YEARS_PAST = tuple(range(datetime.datetime.now().year-100, datetime.datetime.now().year+1))
YEARS_FUTURE = tuple(range(datetime.datetime.now().year, datetime.datetime.now().year+100))
