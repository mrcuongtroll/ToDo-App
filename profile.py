from tkinter import *
from tkinter import ttk
import os
import utils


# Classes
class _ProfileFrame(ttk.Frame):

    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.style = ttk.Style()

        # Account frame: username and password
        self.account_frame = ttk.LabelFrame(self, text='Account', padding=30)
        self.account_frame.grid(row=0, column=0, sticky=N+S+E+W)
        Label(self.account_frame, text='Your account', font='Calibri 20 bold').pack(anchor=W)
        self.account_frame2 = ttk.Frame(self.account_frame, relief=FLAT, padding=10)
        self.account_frame2.pack(anchor=W, fill=BOTH, expand=True)
        ttk.Label(self.account_frame2, text='Username:').grid(row=0, column=0, sticky=W)
        self.username = ttk.Label(self.account_frame2, text='')  # TODO: update
        self.username.grid(row=0, column=1, sticky=W)
        ttk.Label(self.account_frame2, text='Password:').grid(row=1, column=0, sticky=W)
        ttk.Label(self.account_frame2, text='********').grid(row=1, column=1, sticky=W)
        self.change_password_button = ttk.Label(self.account_frame2,
                                                text='Change password',
                                                style='ChangePassword.TLabel')
        self.change_password_button.grid(row=2, column=0, columnspan=2, sticky=W)
        self.change_password_button.bind('<Button-1>', self.change_password)
        self.change_password_button.bind('<Enter>',
                                         lambda e: utils.style_map(self.change_password_button,
                                                                   font='Arial 9 underline')
                                         )
        self.change_password_button.bind('<Leave>',
                                         lambda e: utils.style_map(self.change_password_button,
                                                                   font='Arial 9')
                                         )

        # Information frame: contains information (obviously)
        self.info_frame = ttk.LabelFrame(self, text='Information', padding=30)
        self.info_frame.grid(row=1, column=0, sticky=N+S+E+W)
        Label(self.info_frame, text='Your information', font='Calibri 20 bold').pack(anchor=W)
        self.update_info_button = ttk.Label(self.info_frame,
                                            text='Update information',
                                            style='UpdateInfo.TLabel',
                                            command=None)  # TODO: this
        self.update_info_button.pack(anchor=W)
        self.update_info_button.bind('<Button-1>', self.update_info)
        self.update_info_button.bind('<Enter>',
                                     lambda e: utils.style_map(self.update_info_button,
                                                               font='Arial 9 underline')
                                     )
        self.update_info_button.bind('<Leave>',
                                     lambda e: utils.style_map(self.update_info_button,
                                                               font='Arial 9')
                                     )
        self.info_frame2 = utils.create_info_frame(self.info_frame, editable=False)
        self.info_frame2.pack(anchor=W)
        self.save_info_button = ttk.Button(self.info_frame, text='Save information', command=self.save_info)

        # Configures
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.style.configure('ChangePassword.TLabel', font='Arial 9', foreground='blue')
        self.style.configure('UpdateInfo.TLabel', font='Arial 9', foreground='blue')

    def change_password(self, event=None):
        # TODO: implement this
        return

    def update_info(self, event=None):
        self.info_frame2.set_editable(True)
        self.save_info_button.pack(anchor=W)
        return

    def save_info(self, event=None):
        # TODO: save info to files
        self.info_frame2.set_editable(False)
        self.save_info_button.pack_forget()
        return


# Functions
def create_profile_frame(master=None):
    return _ProfileFrame(master)
