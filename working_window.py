from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import json
import pystray
from PIL import Image
import utils
import data
import profile
import accounts_manager
import todo_list
import login_window


# Classes
class _WorkingWindow(Tk):

    def __init__(self, username, mode='user'):
        super().__init__()
        self.username = username
        self.mode = mode
        self.data_path = os.path.join(os.getcwd(), 'data/')
        self.task_path = os.path.join(self.data_path, 'tasks/')
        self.img_path = os.path.join(os.getcwd(), 'img/')
        with open(os.path.join(self.data_path, 'accounts.bin'), 'rb') as f:
            self.accounts = json.loads(f.read().decode('utf-8'))
        try:
            with open(os.path.join(self.task_path, f'{self.username}.bin'), 'rb') as f:
                self.tasks = json.loads(f.read().decode('utf-8'))
        except FileNotFoundError:
            self.tasks = data.INIT_TASKS

        # root window.
        self.title('ToDo List')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'640x480+{int(screen_width / 2 - 320)}+{int(screen_height / 2 - 240)}')
        self.state('zoomed')
        # We need a ttk.Style object to manage the style of widgets
        self.style = ttk.Style(self)

        # Menu: including menus
        self.menu = Menu(self, tearoff=False)
        self.config(menu=self.menu)
        # File menu: contains options like logout, exit
        self.file_menu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Refresh',
                                   command=lambda: (self.todo_frame.refresh(), self.accounts_manager_frame.refresh())
                                   )
        self.file_menu.add_command(label='Minimize to system tray', command=self.minimize_to_systray)
        self.file_menu.add_command(label='Log out', command=self.logout)
        self.file_menu.add_command(label='Exit', command=self.destroy)
        # Edit menu:
        # self.edit_menu = Menu(self.menu, tearoff=False)
        # self.menu.add_cascade(label='Edit', menu=self.edit_menu)
        # TODO: add more stuff here

        # Notebook to switch between frames:
        self.notebook = ttk.Notebook(self, padding=5)
        self.notebook.pack(expand=True, side=LEFT, fill=BOTH, anchor=N+W)
        self.notebook.enable_traversal()    # (Shift) + Ctrl + Tab
        # To do list (The "main" working frame)
        self.todo_frame = todo_list.create_todo_frame(self.notebook,
                                                      username=self.username,
                                                      tasks_data=self.tasks)
        self.notebook.add(self.todo_frame, text='To do list')
        # Profile: The user can view their profile info here
        self.profile_frame = profile.create_profile_frame(self.notebook,
                                                          accounts_data=self.accounts,
                                                          username=self.username)
        self.notebook.add(self.profile_frame, text='Your profile')
        self.logout_button = ttk.Button(self.profile_frame, text='Log out', command=lambda: self.logout())
        self.logout_button.grid(row=2, column=0, sticky=E)
        # Accounts manager: For the admin to manage user accounts
        if self.mode == 'admin':
            self.accounts_manager_frame = accounts_manager.create_accounts_manager_frame(self.notebook,
                                                                                         accounts_data=self.accounts)
            self.notebook.add(self.accounts_manager_frame, text='Manage user accounts')

        # main loop
        self.mainloop()

    def destroy(self):
        with open(os.path.join(self.data_path, 'accounts.bin'), 'wb') as f:
            f.write(json.dumps(self.accounts).encode('utf-8'))
        with open(os.path.join(self.task_path, f'{self.username}.bin'), 'wb') as f:
            f.write(json.dumps(self.tasks).encode('utf-8'))
        minimize = messagebox.askyesno('Exit',
                                       'Do you want to minimize to system tray?\nYes: Minimize\nNo: Exit program')
        if minimize:
            self.minimize_to_systray()
        else:
            super().destroy()

    def logout(self, event=None):
        self.accounts['stay_signed_in'] = None
        with open(os.path.join(self.data_path, 'accounts.bin'), 'wb') as f:
            f.write(json.dumps(self.accounts).encode('utf-8'))
        with open(os.path.join(self.task_path, f'{self.username}.bin'), 'wb') as f:
            f.write(json.dumps(self.tasks).encode('utf-8'))
        super().destroy()
        login_window.create_login_window()

    def quit_window(self, icon, item):
        icon.stop()
        super().destroy()

    def show_window(self, icon, item):
        icon.stop()
        self.after(0, self.deiconify)
        self.state('zoomed')

    def minimized_logout(self, icon, item):
        icon.stop()
        self.after(0, self.logout)

    def minimize_to_systray(self):
        self.withdraw()
        image = Image.open(os.path.join(self.img_path, 'systray_icon.ico'))
        menu = (pystray.MenuItem('Show window', self.show_window),
                pystray.MenuItem('Log out', self.minimized_logout),
                pystray.MenuItem('Exit', self.quit_window))
        icon = pystray.Icon('name', image, 'To-do list app', menu)
        icon.run()


# Functions
def create_working_window(username, mode='user'):
    _WorkingWindow(username=username, mode=mode)
