from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import datetime
import calendar
import random
import data


# Constants:
SIGN_UP = 'sign up'
ADD_USER = 'add user'
VIEW_USER = 'view_user'
ADD = 'add'
VIEW = 'view'
DAYS_31 = tuple(range(1, 32))
DAYS_30 = tuple(range(1, 31))
DAYS_29 = tuple(range(1, 30))
DAYS_28 = tuple(range(1, 29))
MONTHS_FULL = tuple(calendar.month_name[i] for i in range(1, 13))
MONTHS_SHORT = tuple(calendar.month_abbr[i] for i in range(1, 13))
YEARS_PAST = tuple(range(datetime.datetime.now().year-100, datetime.datetime.now().year+1))
YEARS_FUTURE = tuple(range(datetime.datetime.now().year, datetime.datetime.now().year+100))
REPEAT_OPTIONS = ('None', 'Daily', 'Weekly', 'Monthly', 'Annually')
REPEAT_DAYS = {'None': 0,
               'Daily': 1,
               'Weekly': 7,
               'Monthly': 30,
               'Annually': 365}
DAYS_REPEAT = {0: 'None',
               1: 'Daily',
               7: 'Weekly',
               30: 'Monthly',
               365: 'Annually'}


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
    # Used to create Sign up form, Add user form and User's details form
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
        restrict = messagebox.askyesno('Restrict account',
                                       f'Are you sure you want to restrict {self.username} until {restriction}?')
        self.lift()
        if restrict:
            self.accounts['accounts'][self.username]['restriction'] = restriction
            self.date_entry.config(state=DISABLED)
            self.restrict_button.config(state=DISABLED)
            self.restrict_remove_button.config(state=NORMAL)
        return

    def remove_restriction(self, event=None):
        remove = messagebox.askyesno('Remove restriction',
                                     f'Are you sure you want to lift restriction from {self.username}?')
        self.lift()
        if remove:
            self.accounts['accounts'][self.username]['restriction'] = None
            self.date_entry.config(state=NORMAL)
            self.restrict_remove_button.config(state=DISABLED)
            self.restrict_button.config(state=NORMAL)
        return


class _TaskFormWindow(Toplevel):

    def __init__(self, master=None, username=None, tasks_data: dict = None, mode=ADD,
                 editable=True, task_name=None):
        super().__init__()
        self.master = master
        self.username = username
        self.tasks = tasks_data
        self.mode = mode
        self.task_name = task_name
        if mode == VIEW:
            assert task_name is not None, 'Task name must be provided in view mode'

        # Basic setups
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'640x640+{int(screen_width / 2 - 320)}+{int(screen_height / 2 - 320)}')
        self.resizable(False, False)
        self.style = ttk.Style(self)

        # The title
        self.label_frame = ttk.Frame(self, relief=FLAT, padding=20)
        self.label_frame.pack()
        if self.mode == ADD:
            self.label = ttk.Label(self.label_frame, text='Add new task', style='TaskForm.TLabel')
        elif self.mode == VIEW:
            self.label = ttk.Label(self.label_frame, text='Task details', style='TaskForm.TLabel')
        self.label.pack()

        # Task information
        self.main_frame = ttk.Frame(self, relief=GROOVE, padding=5)
        self.main_frame.pack(fill=BOTH, expand=True)
        # Task name:
        self.name_frame = ttk.Frame(self.main_frame, relief=FLAT, padding=5)
        self.name_frame.pack(fill=X)
        ttk.Label(self.name_frame, text='Task name*: ', padding=5).grid(row=0, column=0, sticky=W)
        self.task_name_entry = ttk.Entry(self.name_frame, width=30)
        self.task_name_entry.grid(row=0, column=1, sticky=W)
        self.finished_var = IntVar(self)
        if self.mode == VIEW:
            self.finished_checkbox = ttk.Checkbutton(self.name_frame,
                                                     text='Finished',
                                                     padding=5,
                                                     variable=self.finished_var)
            self.finished_checkbox.grid(row=1, column=0, columnspan=2, sticky=W)
        # Datetime
        self.time_frame = ttk.Frame(self.main_frame, relief=FLAT, padding=5)
        self.time_frame.pack(fill=X)
        ttk.Label(self.time_frame, text='Date*: ', padding=5).grid(row=0, column=0, sticky=W)
        self.date_entry = tkcalendar.DateEntry(self.time_frame)
        self.date_entry.grid(row=0, column=1, sticky=W)
        self.start_var = IntVar(self)
        if self.mode == ADD:
            self.start_checkbox = ttk.Checkbutton(self.time_frame,
                                                  text='Start time: ',
                                                  padding=5,
                                                  variable=self.start_var)
            self.start_checkbox.grid(row=1, column=0, sticky=W)
            self.start_checkbox.state(['!alternate'])
        elif self.mode == VIEW:
            ttk.Label(self.time_frame, text='Start time: ', padding=5).grid(row=1, column=0, sticky=W)
        self.start_clock = _SpinClock(self.time_frame)
        self.start_clock.grid(row=1, column=1, sticky=W)
        self.end_var = IntVar(self)
        if self.mode == ADD:
            self.end_checkbox = ttk.Checkbutton(self.time_frame,
                                                text='End time: ',
                                                padding=5,
                                                variable=self.end_var)
            self.end_checkbox.grid(row=2, column=0, sticky=W)
            self.end_checkbox.state(['!alternate'])
        elif self.mode == VIEW:
            ttk.Label(self.time_frame, text='End time: ', padding=5).grid(row=2, column=0, sticky=W)
        self.end_clock = _SpinClock(self.time_frame)
        self.end_clock.grid(row=2, column=1, sticky=W)
        ttk.Label(self.time_frame, text='Repeatable: ').grid(row=3, column=0, sticky=W)
        self.repeat_var = StringVar(self)
        self.repeat_option = ttk.OptionMenu(self.time_frame,
                                            self.repeat_var,
                                            'None',
                                            *REPEAT_OPTIONS)
        self.repeat_option.grid(row=3, column=1, sticky=W)
        # Location
        self.location_frame = ttk.Frame(self.main_frame, relief=FLAT, padding=5)
        self.location_frame.pack(fill=X)
        ttk.Label(self.location_frame, text='Location: ', padding=5).grid(row=0, column=0, sticky=W)
        self.location_entry = ttk.Entry(self.location_frame, width=60)
        self.location_entry.grid(row=0, column=1, sticky=W)
        # Note
        self.note_frame = ttk.Frame(self.main_frame, relief=FLAT, padding=5)
        self.note_frame.pack(fill=X)
        ttk.Label(self.note_frame, text='Note: ', padding=5).grid(row=0, column=0, sticky=W)
        self.note_yscrollbar = ttk.Scrollbar(self.note_frame, orient=VERTICAL)
        self.note_yscrollbar.grid(row=1, column=1, stick=N+S+E)
        self.note_entry = Text(self.note_frame,
                               height=10,
                               wrap=WORD,
                               font='Times 12',
                               yscrollcommand=self.note_yscrollbar.set)
        self.note_yscrollbar.config(command=self.note_entry.yview)
        self.note_entry.grid(row=1, column=0, sticky=E+W)
        self.note_frame.rowconfigure(index=1, weight=1)
        self.note_frame.columnconfigure(index=0, weight=1)

        # Buttons
        self.button_frame = ttk.Frame(self, relief=FLAT, padding=10)
        self.button_frame.pack()
        if self.mode == ADD:
            self.add_button = ttk.Button(self.button_frame,
                                         text='Add task',
                                         command=self.add_task)
            self.add_button.pack()
        elif self.mode == VIEW:
            self.edit_button = ttk.Button(self.button_frame,
                                          text='Edit',
                                          width=10,
                                          command=self.edit_task)
            self.edit_button.grid(row=0, column=0, sticky=W)
            self.save_button = ttk.Button(self.button_frame,
                                          text='Save',
                                          width=10,
                                          command=self.update_task_info,
                                          state=DISABLED)
            self.save_button.grid(row=0, column=1, sticky=W)
            self.cancel_button = ttk.Button(self.button_frame,
                                            text='Cancel',
                                            width=10,
                                            command=self.destroy)
            self.cancel_button.grid(row=1, column=0, columnspan=2)

        # Theme and style
        self.style.configure('TaskForm.TLabel', font='Calibri 30')

        # Configures
        if self.mode == VIEW:
            self.view_mode()
        self.set_editable(editable)

    def set_editable(self, editable=True, event=None):
        if editable:
            state = NORMAL
        else:
            state = DISABLED
        self.task_name_entry.config(state=state)
        self.date_entry.config(state=state)
        self.start_clock.change_state(state=state)
        self.end_clock.change_state(state=state)
        self.repeat_option.config(state=state)
        self.location_entry.config(state=state)
        self.note_entry.config(state=state)
        if self.mode == VIEW:
            self.finished_checkbox.config(state=state)
        return

    def add_task(self, event=None):
        task_name = self.task_name_entry.get()
        date = self.date_entry.get_date().strftime('%m/%d/%Y')
        if not task_name or not date:
            messagebox.showerror('Error', 'Task name and date are required')
            self.lift()
        else:
            # Get the info
            start_time = '00:00:00'
            if self.start_var.get():
                try:
                    start_time = self.start_clock.get_time()
                except ValueError:
                    messagebox.showerror('Error', 'Invalid start time')
                    self.lift()
            end_time = '23:59:59'
            if self.end_var.get():
                try:
                    end_time = self.end_clock.get_time()
                except ValueError:
                    messagebox.showerror('Error', 'Invalid end time')
                    self.lift()
            repeat = REPEAT_DAYS[self.repeat_var.get()]
            location = self.location_entry.get() if self.location_entry.get() else None
            note = self.note_entry.get(1.0, END).strip() if self.note_entry.get(1.0, END) else None
            # Check for time overlap
            time_overlap_tag = None
            count = 1
            for available_task in self.tasks['tasks_list'].keys():
                if available_task == task_name:
                    messagebox.showerror('Error', 'Task name already exists')
                    self.lift()
                    return
                if self.tasks['tasks_list'][available_task]['date'] == date:
                    start1 = start_time
                    start1 = datetime.datetime.strptime(date + ' ' + start1, '%m/%d/%Y %H:%M:%S')
                    end1 = end_time
                    end1 = datetime.datetime.strptime(date + ' ' + end1, '%m/%d/%Y %H:%M:%S')
                    start2 = self.tasks['tasks_list'][available_task]['start'] \
                        if self.tasks['tasks_list'][available_task]['start'] else '00:00:00'
                    start2 = datetime.datetime.strptime(date + ' ' + start2, '%m/%d/%Y %H:%M:%S')
                    end2 = self.tasks['tasks_list'][available_task]['end'] \
                        if self.tasks['tasks_list'][available_task]['end'] else '23:59:59'
                    end2 = datetime.datetime.strptime(date + ' ' + end2, '%m/%d/%Y %H:%M:%S')
                    overlap = min(end1, end2) - max(start1, start2)
                    if overlap.days >= 0:
                        self.tasks['tasks_list'][available_task]['time_overlap_tag'] = date
                        time_overlap_tag = date
                        count += 1
            if time_overlap_tag is not None:
                if time_overlap_tag in self.tasks['time_overlap_tags'].keys():
                    self.tasks['time_overlap_tags'][time_overlap_tag] += 1
                else:
                    self.tasks['time_overlap_tags'][time_overlap_tag] = count
            # Add new task
            new_task = data.Task(username=self.username,
                                 date=date,
                                 start=start_time,
                                 end=end_time,
                                 repeat=repeat,
                                 location=location,
                                 note=note,
                                 time_overlap_tag=time_overlap_tag)
            self.tasks['tasks_list'][task_name] = new_task.to_dict()
            messagebox.showinfo('Success', 'New task has been added successfully')
            self.destroy()
        return

    def edit_task(self, event=None):
        self.set_editable(True)
        self.task_name_entry.config(state=DISABLED)     # The task name must not change
        self.edit_button.config(state=DISABLED)
        self.save_button.config(state=NORMAL)
        return

    def update_task_info(self, event=None):
        # update info
        date = self.date_entry.get_date().strftime('%m/%d/%Y')
        self.tasks['tasks_list'][self.task_name]['date'] = date
        try:
            self.tasks['tasks_list'][self.task_name]['start'] = self.start_clock.get_time()
        except ValueError:
            messagebox.showerror('Error', 'Invalid start time')
            self.lift()
            return
        try:
            self.tasks['tasks_list'][self.task_name]['end'] = self.end_clock.get_time()
        except ValueError:
            messagebox.showerror('Error', 'Invalid end time')
            self.lift()
            return
        repeat = self.repeat_var.get()
        self.tasks['tasks_list'][self.task_name]['repeat'] = REPEAT_DAYS[repeat]
        location = self.location_entry.get() if self.location_entry.get() else None
        self.tasks['tasks_list'][self.task_name]['location'] = location
        note = self.note_entry.get(1.0, END).strip() if self.note_entry.get(1.0, END) else None
        self.tasks['tasks_list'][self.task_name]['note'] = note
        if self.finished_var.get():
            self.tasks['tasks_list'][self.task_name]['finished'] = True
            now = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
            self.tasks['tasks_list'][self.task_name]['finish_date'] = now
        else:
            self.tasks['tasks_list'][self.task_name]['finished'] = False
            self.tasks['tasks_list'][self.task_name]['finish_date'] = None
        # Change everything pack to view mode
        self.view_mode()
        self.set_editable(False)
        self.edit_button.config(state=NORMAL)
        self.save_button.config(state=DISABLED)
        return

    def view_mode(self, event=None):
        task_name = self.task_name
        self.task_name_entry.delete(0, END)
        self.task_name_entry.insert(0, task_name)
        date = self.tasks['tasks_list'][task_name]['date']
        date = datetime.datetime.strptime(date, '%m/%d/%Y')
        self.date_entry.set_date(date)
        start_time = self.tasks['tasks_list'][task_name]['start']
        self.start_clock.set_time(start_time)
        end_time = self.tasks['tasks_list'][task_name]['end']
        self.end_clock.set_time(end_time)
        repeat = self.tasks['tasks_list'][task_name]['repeat']
        self.repeat_var.set(DAYS_REPEAT[repeat])
        location = self.tasks['tasks_list'][task_name]['location'] \
            if self.tasks['tasks_list'][task_name]['location'] else None
        self.location_entry.delete(0, END)
        self.location_entry.insert(0, location)
        note = self.tasks['tasks_list'][task_name]['note'] if self.tasks['tasks_list'][task_name]['note'] else None
        self.note_entry.delete(1.0, END)
        self.note_entry.insert(END, note)
        finished = self.tasks['tasks_list'][task_name]['finished']
        if finished and self.mode == VIEW:
            # self.finished_checkbox.state(['selected'])
            self.finished_var.set(1)
        elif not finished and self.mode == VIEW:
            # self.finished_checkbox.state(['!alternate'])
            self.finished_var.set(0)
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


class _SpinClock(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.hour_spinner = ttk.Spinbox(self, from_=0, to=23,
                                        wrap=True,
                                        width=5,
                                        state='readonly',
                                        justify=CENTER)
        self.hour_spinner.grid(row=0, column=0)
        ttk.Label(self, text='h', padding=2).grid(row=0, column=1)
        self.minute_spinner = ttk.Spinbox(self, from_=0, to=59,
                                          wrap=True,
                                          width=5,
                                          state='readonly',
                                          justify=CENTER)
        self.minute_spinner.grid(row=0, column=2)
        ttk.Label(self, text='m', padding=2).grid(row=0, column=3)
        self.second_spinner = ttk.Spinbox(self, from_=0, to=59,
                                          wrap=True,
                                          width=5,
                                          state='readonly',
                                          justify=CENTER)
        self.second_spinner.grid(row=0, column=4)
        ttk.Label(self, text='s', padding=2).grid(row=0, column=5)

    def get_time(self, event=None):
        # Format: %H:%M:%S
        hour = self.hour_spinner.get()
        minute = self.minute_spinner.get()
        second = self.second_spinner.get()
        time = f'{hour}:{minute}:{second}'
        time = datetime.datetime.strptime(time, '%H:%M:%S').time()
        time = time.strftime('%H:%M:%S')
        return time

    def change_state(self, state):
        self.hour_spinner.config(state=state)
        self.minute_spinner.config(state=state)
        self.second_spinner.config(state=state)
        return

    def set_time(self, time: str):
        time = time.split(':')
        self.hour_spinner.set(int(time[0]))
        self.minute_spinner.set(int(time[1]))
        self.second_spinner.set(int(time[2]))
        return


# Functions
def create_info_frame(master=None, editable=True, acc_info=None):
    return _InfoFrame(master, editable, acc_info)


def create_user_form(master=None, accounts_data=None, mode=SIGN_UP, deiconify_master=True, username=None):
    return _UserFormWindow(master, accounts_data, mode, deiconify_master, username)


def create_task_form(master=None, username=None, tasks_data=None, mode=ADD, editable=True, task_name=None):
    return _TaskFormWindow(master, username, tasks_data, mode, editable, task_name)


def input_string_dialog(master=None, title='', prompt='', show='*'):
    dialog = _InputDialog(master, title, prompt, show)
    return dialog.text.get()


def random_color():
    de_ = ("%02x" % random.randint(0, 255))
    # re_ = ("%02x" % random.randint(0, 255))
    re_ = '95'  # We'll only choose light colors
    we_ = ("%02x" % random.randint(0, 255))
    ge_ = "#"
    color = ge_ + de_ + re_ + we_
    return color


def style_map(widget, **kwargs):
    for attr, value in kwargs.items():
        widget[attr] = value
