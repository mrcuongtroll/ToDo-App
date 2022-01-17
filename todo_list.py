from tkinter import *
from tkinter import ttk
import ttkwidgets
import os
import utils
import tkcalendar


# Classes
class _TodoFrame(ttk.Frame):

    def __init__(self, master=None):
        super().__init__()
        self.master = master

        # Control frame: Contains component (buttons, calendar,...) to control the workflow
        self.control_frame = ttk.Frame(self, padding=5)
        self.control_frame.grid(row=0, column=0, sticky=N+E+W)
        # Calendar
        self.cal = tkcalendar.Calendar(self.control_frame, selectmode='day')
        self.cal.grid(row=0, column=0, sticky=N+S+E+W)
        # Buttons
        self.button_frame = ttk.Frame(self.control_frame, padding=20)
        self.button_frame.grid(row=0, column=1, sticky=N+S+E+W)
        self.add_button = ttk.Button(self.button_frame,
                                     text='Add new task',
                                     width=20,
                                     command=None)  # TODO: this
        self.add_button.pack(pady=2)
        self.delete_button = ttk.Button(self.button_frame,
                                        text='Delete task',
                                        width=20,
                                        state=DISABLED,
                                        command=None)    # TODO: this
        self.delete_button.pack(pady=2)
        self.view_button = ttk.Button(self.button_frame,
                                      text='View details',
                                      width=20,
                                      state=DISABLED,
                                      command=None)     # TODO: this
        self.view_button.pack(pady=2)
        self.save_button = ttk.Button(self.button_frame,
                                      text='Save',
                                      width=20,
                                      command=None)     # TODO: this
        self.save_button.pack(pady=2)
        # Upcoming task
        self.upcoming_frame = ttk.Frame(self.control_frame, relief=GROOVE, padding=30)
        self.upcoming_frame.grid(row=0, column=2, sticky=N+S+E+W)
        self.control_frame.columnconfigure(index=2, weight=1)
        self.control_frame.rowconfigure(index=0, weight=1)
        Label(self.upcoming_frame, text='Upcoming task', font='Calibri 20 bold').pack(anchor=W)
        self.upcoming_frame2 = ttk.Frame(self.upcoming_frame, relief=FLAT)
        self.upcoming_frame2.pack(anchor=W, fill=BOTH, expand=True)
        ttk.Label(self.upcoming_frame2, text='Task name:').grid(row=1, column=0, sticky=W)
        self.task_name = ttk.Label(self.upcoming_frame2, text='')    # TODO: update
        self.task_name.grid(row=1, column=1, sticky=W)
        ttk.Label(self.upcoming_frame2, text='Time:').grid(row=2, column=0, sticky=W)
        self.task_time = ttk.Label(self.upcoming_frame2, text='')    # TODO: update
        self.task_time.grid(row=2, column=1, sticky=W)
        ttk.Label(self.upcoming_frame2, text='Location:').grid(row=3, column=0, sticky=W)
        self.task_location = ttk.Label(self.upcoming_frame2, text='')    # TODO: update
        self.task_location.grid(row=3, column=1, sticky=W)
        ttk.Label(self.upcoming_frame2, text='Note:').grid(row=4, column=0, sticky=W)
        self.task_note = ttk.Label(self.upcoming_frame2, text='')    # TODO: update
        self.task_note.grid(row=4, column=1, sticky=W)

        # List frame: Contains our to do list
        self.list_frame = ttk.Frame(self, padding=5, relief=GROOVE)
        self.list_frame.grid(row=1, column=0, sticky=N+S+E+W)
        self.list_frame.columnconfigure(index=0, weight=1)
        self.list_frame.rowconfigure(index=0, weight=1)
        self.list_frame.rowconfigure(index=1, weight=1)
        # Unfinished list: contains unfinished task
        self.unfinished_frame = ttk.LabelFrame(self.list_frame, text='Unfinished tasks', padding=2)
        self.unfinished_frame.grid(row=0, column=0, sticky=N+S+E+W)
        self.unfinished_frame.rowconfigure(index=0, weight=1)
        self.unfinished_frame.columnconfigure(index=0, weight=1)
        self.unfinished_yscrollbar = ttk.Scrollbar(self.unfinished_frame, orient=VERTICAL)
        self.unfinished_yscrollbar.grid(row=0, column=1, sticky=N+S+E)
        self.unfinished_xscrollbar = ttk.Scrollbar(self.unfinished_frame, orient=HORIZONTAL)
        self.unfinished_xscrollbar.grid(row=1, column=0, sticky=S+E+W)
        self.unfinished_list = ttkwidgets.CheckboxTreeview(self.unfinished_frame,
                                                           selectmode=BROWSE,
                                                           xscrollcommand=self.unfinished_xscrollbar.set,
                                                           yscrollcommand=self.unfinished_yscrollbar.set)
        self.unfinished_list.grid(row=0, column=0, sticky=N+S+E+W)
        self.unfinished_xscrollbar.config(command=self.unfinished_list.xview)
        self.unfinished_yscrollbar.config(command=self.unfinished_list.yview)
        self.unfinished_list['columns'] = ('Task', 'Start date', 'End date', 'Location', 'Status')
        self.unfinished_list.column('#0', width=60, minwidth=60, stretch=NO, anchor=CENTER)
        self.unfinished_list.heading('#0', text='Finished')
        for column in self.unfinished_list['columns']:
            self.unfinished_list.column(column, minwidth=100, anchor=W)
            self.unfinished_list.heading(column, text=column)
        # Finished list: contains finished task
        self.finished_frame = ttk.LabelFrame(self.list_frame, text='Finished tasks', padding=2)
        self.finished_frame.grid(row=1, column=0, sticky=N+S+E+W, pady=5)
        self.finished_frame.rowconfigure(index=0, weight=1)
        self.finished_frame.columnconfigure(index=0, weight=1)
        self.finished_yscrollbar = ttk.Scrollbar(self.finished_frame, orient=VERTICAL)
        self.finished_yscrollbar.grid(row=0, column=1, sticky=N+S+E)
        self.finished_xscrollbar = ttk.Scrollbar(self.finished_frame, orient=HORIZONTAL)
        self.finished_xscrollbar.grid(row=1, column=0, sticky=S+E+W)
        self.finished_list = ttk.Treeview(self.finished_frame,
                                          selectmode=BROWSE,
                                          xscrollcommand=self.finished_xscrollbar.set,
                                          yscrollcommand=self.finished_yscrollbar.set)
        self.finished_list.grid(row=0, column=0, sticky=N+S+E+W)
        self.finished_xscrollbar.config(command=self.finished_list.xview)
        self.finished_yscrollbar.config(command=self.finished_list.yview)
        self.finished_list['columns'] = ('Task', 'Start date', 'End date', 'Location', 'Finish date', 'Finished')
        self.finished_list.column('#0', width=0, minwidth=0, stretch=NO)
        for column in self.finished_list['columns']:
            self.finished_list.column(column, minwidth=40)
            self.finished_list.heading(column, text=column)

        # Configures
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)


# Functions
def create_todo_frame(master=None):
    return _TodoFrame(master)
