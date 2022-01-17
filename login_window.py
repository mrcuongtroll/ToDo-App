from tkinter import *
from tkinter import ttk
import os
import datetime
import calendar
from working_window import *
import utils


# Classes
class _LoginWindow(Tk):
    # The constants
    USERNAME_DEFAULT_TEXT = 'Enter your username'
    PASSWORD_DEFAULT_TEXT = 'Enter your password'

    def __init__(self):
        super().__init__()
        self.data_path = os.path.join(os.getcwd(), 'data/')
        # TODO: data

        # root window.
        self.title('ToDo List - Login')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'640x480+{int(screen_width/2-320)}+{int(screen_height/2-240)}')
        self.resizable(False, False)
        # We need a ttk.Style object to manage the style of widgets
        self.style = ttk.Style(self)

        # The title of the app
        self.label_frame = ttk.Frame(self, relief=FLAT, padding=40)
        self.label_frame.pack(expand=TRUE)
        self.label = ttk.Label(self.label_frame, text='ToDo List', style='Title.TLabel')
        self.label.pack()
        self.rowconfigure(index=0, weight=1)

        # The login part
        self.lower_frame = ttk.Frame(self, relief=FLAT, padding=40)
        self.lower_frame.pack()
        self.login_frame = ttk.Frame(self.lower_frame, relief=GROOVE, padding=2)
        self.login_frame.pack()
        self.input_frame = ttk.Frame(self.login_frame, relief=FLAT, padding=20)
        self.input_frame.pack()
        # The user enters their username here
        self.username_label = ttk.Label(self.input_frame, text='Username', padding=5)
        self.username_label.grid(row=0, column=0, sticky=E)
        self.username_entry = ttk.Entry(self.input_frame, width=30, style='Username.TEntry')
        self.username_entry.grid(row=0, column=1, sticky=W)
        self.username_entry.bind('<FocusIn>',
                                 lambda e: self.entry_focus_in(self.username_entry,
                                                               'Username.TEntry',
                                                               _LoginWindow.USERNAME_DEFAULT_TEXT,
                                                               event=e)
                                 )
        self.username_entry.bind('<FocusOut>',
                                 lambda e: self.entry_focus_out(self.username_entry,
                                                                'Username.TEntry',
                                                                _LoginWindow.USERNAME_DEFAULT_TEXT,
                                                                event=e)
                                 )
        self.username_entry.bind('<Return>', self.login)
        # The user enters their password here
        self.password_label = ttk.Label(self.input_frame, text='Password', padding=5)
        self.password_label.grid(row=1, column=0, sticky=E)
        self.password_entry = ttk.Entry(self.input_frame, show='*', width=30, style='Password.TEntry')
        self.password_entry.grid(row=1, column=1, sticky=W)
        self.password_entry.bind('<FocusIn>',
                                 lambda e: self.entry_focus_in(self.password_entry,
                                                               'Password.TEntry',
                                                               _LoginWindow.PASSWORD_DEFAULT_TEXT,
                                                               event=e)
                                 )
        self.password_entry.bind('<FocusOut>',
                                 lambda e: self.entry_focus_out(self.password_entry,
                                                                'Password.TEntry',
                                                                _LoginWindow.PASSWORD_DEFAULT_TEXT,
                                                                event=e)
                                 )
        self.password_entry.bind('<Return>', self.login)
        # A checkbox to indicate that the user wants to stay signed in
        self.stay_signed_in = IntVar()
        self.login_checkbox = ttk.Checkbutton(self.input_frame,
                                              text='Stay signed in',
                                              padding=5,
                                              variable=self.stay_signed_in)
        self.login_checkbox.grid(row=2, column=0, columnspan=2)
        self.login_checkbox.state(['!alternate'])
        # The login button
        self.button_frame = ttk.Frame(self.login_frame, relief=FLAT, padding=10)
        self.button_frame.pack()
        self.login_button = ttk.Button(self.button_frame, text='Login', command=self.login)
        self.login_button.pack()
        # Sign up option
        self.signup_button = ttk.Label(self.button_frame,
                                       text="Don't have an account? Sign up!",
                                       style='SignUp.TLabel')
        self.signup_button.pack()
        self.signup_button.bind('<Button-1>', self.signup)
        self.signup_button.bind('<Enter>', lambda e: utils.style_map(self.signup_button, font='Arial 9 underline'))
        self.signup_button.bind('<Leave>', lambda e: utils.style_map(self.signup_button, font='Arial 9'))

        # Style and theme
        self.style.configure('Title.TLabel', font='Calibri 70 bold', foreground='grey')
        self.style.configure('Username.TEntry', foreground='grey')
        self.username_entry.insert(0, _LoginWindow.USERNAME_DEFAULT_TEXT)
        self.style.configure('Password.TEntry', foreground='grey')
        self.password_entry.insert(0, _LoginWindow.PASSWORD_DEFAULT_TEXT)
        self.style.configure('SignUp.TLabel', font='Arial 9', foreground='blue')

        # main loop
        self.mainloop()

    def signup(self, event=None):
        utils.create_user_form(self, mode=utils.SIGN_UP)
        self.withdraw()

    def login(self, event=None):
        # TODO: Write this properly
        self.destroy()
        create_working_window(mode='admin')

    # Entry fields related functions
    def entry_focus_in(self, entry_widget, entry_style, default_text, event=None):
        if entry_widget.get() == default_text:
            entry_widget.delete(0, END)
            self.style.configure(entry_style, foreground='black')

    def entry_focus_out(self, entry_widget, entry_style, default_text, event=None):
        if entry_widget.get() == '':
            self.style.configure(entry_style, foreground='grey')
            entry_widget.insert(0, default_text)


# Functions
def create_login_window():
    return _LoginWindow()