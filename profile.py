from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import utils


# Classes
class _ProfileFrame(ttk.Frame):

    def __init__(self, master=None, accounts_data: dict = None, username=''):
        super().__init__()
        self.username = username
        self.master = master
        self.accounts = accounts_data
        self.style = ttk.Style()

        # Account frame: username and password
        self.account_frame = ttk.LabelFrame(self, text='Account', padding=30)
        self.account_frame.grid(row=0, column=0, sticky=N+S+E+W)
        Label(self.account_frame, text='Your account', font='Calibri 20 bold').pack(anchor=W)
        self.account_frame2 = ttk.Frame(self.account_frame, relief=FLAT, padding=10)
        self.account_frame2.pack(anchor=W, fill=BOTH, expand=True)
        ttk.Label(self.account_frame2, text='Username:').grid(row=0, column=0, sticky=W)
        ttk.Label(self.account_frame2, text=self.username).grid(row=0, column=1, sticky=W)
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
        self.info_frame2 = utils.create_info_frame(self.info_frame,
                                                   editable=False,
                                                   acc_info=accounts_data['accounts'][username])
        self.info_frame2.pack(anchor=W)
        self.save_info_button = ttk.Button(self.info_frame, text='Save information', command=self.save_info)

        # Configures
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.style.configure('ChangePassword.TLabel', font='Arial 9', foreground='blue')
        self.style.configure('UpdateInfo.TLabel', font='Arial 9', foreground='blue')

    def change_password(self, event=None):
        confirm_password = utils.input_string_dialog(self, 'Confirm password', 'Confirm password', show='*')
        if confirm_password:
            if confirm_password != self.accounts['accounts'][self.username]['password']:
                messagebox.showerror('Error', "Your password confirmation doesn't match")
            else:
                new_password = utils.input_string_dialog(self, 'New password', 'New password', show='*')
                if new_password == self.accounts['accounts'][self.username]['password']:
                    messagebox.showerror('Error', "New password must not be the same as old password")
                elif new_password:
                    confirm_new_password = utils.input_string_dialog(self, 'Confirm password',
                                                                     'Confirm new password', show='*')
                    if confirm_new_password:
                        if new_password != confirm_new_password:
                            messagebox.showerror('Error', "Your new password confirmation doesn't match")
                        else:
                            self.accounts['accounts'][self.username]['password'] = new_password
                            messagebox.showinfo('Success', 'Your password has been changed successfully')
        return

    def update_info(self, event=None):
        confirm_password = utils.input_string_dialog(self, 'Confirm password', 'Confirm password', show='*')
        if confirm_password:
            if confirm_password != self.accounts['accounts'][self.username]['password']:
                messagebox.showerror('Error', "Your password confirmation doesn't match")
            else:
                self.info_frame2.set_editable(True)
                self.save_info_button.pack(anchor=W)
        return

    def save_info(self, event=None):
        self.info_frame2.update_info()
        self.info_frame2.set_editable(False)
        self.save_info_button.pack_forget()
        messagebox.showinfo('Success', 'Your information has been updated successfully')
        return


# Functions
def create_profile_frame(master=None, accounts_data=None, username=''):
    return _ProfileFrame(master, accounts_data, username)
