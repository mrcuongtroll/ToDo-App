from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import ttkwidgets
import tkcalendar
import datetime
import os
import utils


# Classes
class _TodoFrame(ttk.Frame):

    def __init__(self, master=None, username='', tasks_data: dict = None):
        super().__init__()
        self.master = master
        self.username = username
        self.tasks = tasks_data
        self.style = ttk.Style(self)

        # Control frame: Contains component (buttons, calendar,...) to control the workflow
        self.control_frame = ttk.Frame(self, padding=5)
        self.control_frame.grid(row=0, column=0, sticky=N+E+W)
        # Calendar
        self.cal = tkcalendar.Calendar(self.control_frame, date_pattern='mm/dd/y', selectmode='day')
        self.cal.grid(row=0, column=0, sticky=N+S+E+W)
        self.cal.bind('<<CalendarSelected>>', self.filter_by_date)
        # Buttons
        self.button_frame = ttk.Frame(self.control_frame, padding=10)
        self.button_frame.grid(row=0, column=1, sticky=N+S+E+W)
        self.refresh_button = ttk.Button(self.button_frame,
                                         text='Refresh',
                                         width=20,
                                         command=self.refresh)
        self.refresh_button.pack(pady=2)
        self.add_button = ttk.Button(self.button_frame,
                                     text='Add new task',
                                     width=20,
                                     command=self.add_task)
        self.add_button.pack(pady=2)
        self.delete_button = ttk.Button(self.button_frame,
                                        text='Delete task',
                                        width=20,
                                        state=DISABLED,
                                        command=self.delete_task)
        self.delete_button.pack(pady=2)
        self.view_button = ttk.Button(self.button_frame,
                                      text='View details',
                                      width=20,
                                      state=DISABLED,
                                      command=self.view_task)
        self.view_button.pack(pady=2)
        self.save_button = ttk.Button(self.button_frame,
                                      text='Save',
                                      width=20,
                                      command=self.save)
        self.save_button.pack(pady=2)
        self.time_overlap_frame = ttk.Frame(self.button_frame, padding=2)
        self.time_overlap_frame.pack(fill=X)
        self.time_overlap_tags = ['None',]
        self.time_overlap_var = StringVar(self)
        ttk.Label(self.time_overlap_frame, text='Filter overlapping').grid(row=0, column=0, sticky=W)
        self.time_overlap_option = ttk.OptionMenu(self.time_overlap_frame,
                                                  self.time_overlap_var,
                                                  'None',
                                                  *self.time_overlap_tags,
                                                  command=self.filter_overlapping)
        self.time_overlap_option.grid(row=0, column=1, sticky=E)
        # Upcoming task
        self.upcoming_frame = ttk.Frame(self.control_frame, relief=GROOVE, padding=30)
        self.upcoming_frame.grid(row=0, column=2, sticky=N+S+E+W)
        self.control_frame.columnconfigure(index=2, weight=1)
        self.control_frame.rowconfigure(index=0, weight=1)
        Label(self.upcoming_frame, text='Upcoming task', font='Calibri 20 bold').pack(anchor=W)
        self.upcoming_frame2 = ttk.Frame(self.upcoming_frame, relief=FLAT)
        self.upcoming_frame2.pack(anchor=W, fill=BOTH, expand=True)
        ttk.Label(self.upcoming_frame2, text='Task name:').grid(row=1, column=0, sticky=W)
        self.task_name = ttk.Label(self.upcoming_frame2, text='')
        self.task_name.grid(row=1, column=1, sticky=W)
        ttk.Label(self.upcoming_frame2, text='Time:').grid(row=2, column=0, sticky=W)
        self.task_time = ttk.Label(self.upcoming_frame2, text='')
        self.task_time.grid(row=2, column=1, sticky=W)
        ttk.Label(self.upcoming_frame2, text='Location:').grid(row=3, column=0, sticky=W)
        self.task_location = ttk.Label(self.upcoming_frame2, text='')
        self.task_location.grid(row=3, column=1, sticky=W)
        ttk.Label(self.upcoming_frame2, text='Note:').grid(row=4, column=0, sticky=W)
        self.task_note = ttk.Label(self.upcoming_frame2, text='')
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
        self.unfinished_list['columns'] = ('Task', 'Date', 'Start', 'End', 'Location', 'Late')
        self.unfinished_list.column('#0', width=60, minwidth=60, stretch=NO, anchor=CENTER)
        self.unfinished_list.heading('#0', text='Finished')
        for column in self.unfinished_list['columns']:
            self.unfinished_list.column(column, minwidth=100, anchor=W)
            self.unfinished_list.heading(column, text=column)
        self.unfinished_list.tag_bind('task', '<Button-1>',
                                      lambda e: (self.deselect_finished(e), self.task_selected(e))
                                      )
        self.unfinished_list.tag_bind('task', '<Double-1>', self.view_task)
        self.unfinished_list.tag_bind('task', '<Return>', self.view_task)
        self.unfinished_list.tag_bind('task', '<Delete>', self.delete_task)
        # Finished list: contains finished task
        self.finished_frame = ttk.LabelFrame(self.list_frame, text='Finished tasks', padding=2)
        self.finished_frame.grid(row=1, column=0, sticky=N+S+E+W, pady=5)
        self.finished_frame.rowconfigure(index=0, weight=1)
        self.finished_frame.columnconfigure(index=0, weight=1)
        self.finished_yscrollbar = ttk.Scrollbar(self.finished_frame, orient=VERTICAL)
        self.finished_yscrollbar.grid(row=0, column=1, sticky=N+S+E)
        self.finished_xscrollbar = ttk.Scrollbar(self.finished_frame, orient=HORIZONTAL)
        self.finished_xscrollbar.grid(row=1, column=0, sticky=S+E+W)
        self.finished_list = ttkwidgets.CheckboxTreeview(self.finished_frame,
                                                         selectmode=BROWSE,
                                                         xscrollcommand=self.finished_xscrollbar.set,
                                                         yscrollcommand=self.finished_yscrollbar.set)
        self.finished_list.grid(row=0, column=0, sticky=N+S+E+W)
        self.finished_xscrollbar.config(command=self.finished_list.xview)
        self.finished_yscrollbar.config(command=self.finished_list.yview)
        self.finished_list['columns'] = ('Task', 'Date', 'Start', 'End', 'Location', 'Finish date')
        self.finished_list.column('#0', width=60, minwidth=60, stretch=NO, anchor=CENTER)
        self.finished_list.heading('#0', text='Finished')
        for column in self.finished_list['columns']:
            self.finished_list.column(column, minwidth=100, anchor=W)
            self.finished_list.heading(column, text=column)
        self.finished_list.tag_bind('task', '<Button-1>',
                                    lambda e: (self.deselect_unfinished(e), self.task_selected(e))
                                    )
        self.finished_list.tag_bind('task', '<Double-1>', self.view_task)
        self.finished_list.tag_bind('task', '<Return>', self.view_task)
        self.finished_list.tag_bind('task', '<Delete>', self.delete_task)

        # Configures
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)

        # Theme and style
        # Make the selection more distinguishable:
        self.style.map("Checkbox.Treeview",
                       fieldbackground=[("selected", 'white')],
                       foreground=[("selected", '#FFFFFF')],
                       background=[("selected", '#000000')],
                       font=[('selected', 'Times 12 bold')])
        self.refresh()

    def refresh(self, event=None):
        # Clear the current lists
        for task in self.unfinished_list.get_children():
            self.unfinished_list.delete(task)
        for task in self.finished_list.get_children():
            self.finished_list.delete(task)
        # Add stuff to the lists
        for task in self.tasks['tasks_list'].keys():
            # Check repeat:
            repeat = self.tasks['tasks_list'][task]['repeat']
            now = datetime.datetime.now()
            if repeat > 0:
                creation_date = self.tasks['tasks_list'][task]['creation_date']
                creation_date = datetime.datetime.strptime(creation_date, '%m/%d/%Y %H:%M:%S')
                if (now - creation_date).days >= repeat:
                    # If it is time to repeat the task, then update the date, creation date and finish state
                    date = self.tasks['tasks_list'][task]['date']
                    date = datetime.datetime.strptime(date, '%m/%d/%Y').date()
                    date = date + datetime.timedelta(days=repeat)
                    date = date.strftime('%m/%d/%Y')
                    self.tasks['tasks_list'][task]['date'] = date
                    self.tasks['tasks_list'][task]['creation_date'] = now.strftime('%m/%d/%Y %H:%M:%S')
                    self.tasks['tasks_list'][task]['finished'] = False
                    self.tasks['tasks_list'][task]['finish_date'] = None
            # This value is required when adding task => No need to check for null
            task_name = task
            # This value is required when adding task => No need to check for null
            date = self.tasks['tasks_list'][task]['date']
            start_time = self.tasks['tasks_list'][task]['start']
            end_time = self.tasks['tasks_list'][task]['end']
            location = self.tasks['tasks_list'][task]['location'] if self.tasks['tasks_list'][task]['location'] else ''
            # Check if the user is already late for the task
            deadline = datetime.datetime.strptime(date + ' ' + end_time, '%m/%d/%Y %H:%M:%S')
            if deadline > now:
                self.tasks['tasks_list'][task]['late'] = False
            else:
                self.tasks['tasks_list'][task]['late'] = True
            late = self.tasks['tasks_list'][task]['late']
            finished = self.tasks['tasks_list'][task]['finished']
            finish_date = self.tasks['tasks_list'][task]['finish_date'] \
                if self.tasks['tasks_list'][task]['finish_date'] else ''
            time_overlap_tag = self.tasks['tasks_list'][task]['time_overlap_tag']     # Can be None
            if not finished:
                self.unfinished_list.insert(parent='',
                                            iid=task_name,
                                            index=END,
                                            values=(task_name, date, start_time, end_time, location, late),
                                            tags=('task',))
                self.unfinished_list.change_state(task_name, 'unchecked')
                if time_overlap_tag is not None:
                    self.unfinished_list.tag_add(task_name, time_overlap_tag)
            else:
                self.finished_list.insert(parent='',
                                          iid=task_name,
                                          index=END,
                                          values=(task_name, date, start_time, end_time, location, finish_date),
                                          tags=('task',))
                self.finished_list.change_state(task_name, 'checked')
                if time_overlap_tag is not None:
                    self.finished_list.tag_add(task_name, time_overlap_tag)
        # Color tasks with overlapping time:
        for tag in self.tasks['time_overlap_tags'].keys():
            color = utils.random_color()
            self.unfinished_list.tag_configure(tag, background=color)
        # Show currently upcoming task:
        self.display_upcoming()
        # Remove some buttons:
        self.delete_button.config(state=DISABLED)
        self.view_button.config(state=DISABLED)
        # Update overlapping filter
        self.time_overlap_tags = ['None'] + list(self.tasks['time_overlap_tags'].keys())
        self.time_overlap_option = ttk.OptionMenu(self.time_overlap_frame,
                                                  self.time_overlap_var,
                                                  self.time_overlap_var.get(),
                                                  *self.time_overlap_tags,
                                                  command=self.filter_overlapping)
        self.time_overlap_option.grid(row=0, column=1, sticky=E)
        return

    def display_upcoming(self, event=None):
        now = datetime.datetime.now()
        current_time = None
        upcoming_task = None
        # Clear info
        self.task_name.config(text='')
        self.task_time.config(text='')
        self.task_location.config(text='')
        self.task_note.config(text='')
        # Search for the nearest deadline
        for task in self.tasks['tasks_list'].keys():
            if not self.tasks['tasks_list'][task]['finished']:
                date = self.tasks['tasks_list'][task]['date']
                start = self.tasks['tasks_list'][task]['start']
                time = datetime.datetime.strptime(date + ' ' + start, '%m/%d/%Y %H:%M:%S')
                if time > now:
                    if current_time is None:
                        current_time = time
                        upcoming_task = task
                    elif time < current_time:
                        current_time = time
                        upcoming_task = task
        # Show upcoming task
        if upcoming_task:
            self.task_name.config(text=upcoming_task)
            date = self.tasks['tasks_list'][upcoming_task]['date']
            start = self.tasks['tasks_list'][upcoming_task]['start']
            time = date + ' ' + start
            self.task_time.config(text=time)
            location = self.tasks['tasks_list'][upcoming_task]['location'] \
                if self.tasks['tasks_list'][upcoming_task]['location'] else ''
            self.task_location.config(text=location)
            note = self.tasks['tasks_list'][upcoming_task]['note'] \
                if self.tasks['tasks_list'][upcoming_task]['note'] else ''
            self.task_note.config(text=note)
        return

    def deselect_finished(self, event=None):
        for task in self.finished_list.selection():
            self.finished_list.selection_remove(task)
        return

    def deselect_unfinished(self, event=None):
        for task in self.unfinished_list.selection():
            self.unfinished_list.selection_remove(task)
        return

    def add_task(self, event=None):
        form = utils.create_task_form(master=self,
                                      username=self.username,
                                      tasks_data=self.tasks)
        self.wait_window(form)
        self.refresh()
        return

    def delete_task(self, event=None):
        task_name = None
        if self.unfinished_list.selection():
            task_name = self.unfinished_list.selection()[0]
        elif self.finished_list.selection():
            task_name = self.finished_list.selection()[0]
        if task_name:
            delete = messagebox.askyesno('Delete task', f'Do you want to delete {task_name}?')
            if delete:
                time_overlap_tag = self.tasks['tasks_list'][task_name]['time_overlap_tag']
                if time_overlap_tag:
                    self.tasks['time_overlap_tags'][time_overlap_tag] -= 1
                    if self.tasks['time_overlap_tags'][time_overlap_tag] <= 1:
                        for other_task in self.tasks['tasks_list'].keys():
                            if self.tasks['tasks_list'][other_task]['time_overlap_tag'] == time_overlap_tag:
                                self.tasks['tasks_list'][other_task]['time_overlap_tag'] = None
                del self.tasks['tasks_list'][task_name]
                self.refresh()
        return

    def view_task(self, event=None):
        task_name = None
        if self.unfinished_list.selection():
            task_name = self.unfinished_list.selection()[0]
        elif self.finished_list.selection():
            task_name = self.finished_list.selection()[0]
        if task_name:
            form = utils.create_task_form(master=self,
                                          tasks_data=self.tasks,
                                          mode=utils.VIEW,
                                          editable=False,
                                          task_name=task_name)
            self.wait_window(form)
            self.refresh()
        return

    def save(self, event=None):
        # Mark all checked rows from unfinished list as finished
        finished = self.unfinished_list.get_checked()
        finish_date = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        for task_name in finished:
            self.tasks['tasks_list'][task_name]['finished'] = True
            self.tasks['tasks_list'][task_name]['finish_date'] = finish_date
        # Mark all unchecked rows from finished list as unfinished
        checked = self.finished_list.get_checked()
        finished = self.finished_list.get_children()
        unfinished = [task for task in finished if task not in checked]
        for task_name in unfinished:
            self.tasks['tasks_list'][task_name]['finished'] = False
            self.tasks['tasks_list'][task_name]['finish_date'] = None
        messagebox.showinfo('Success', 'Saved successfully')
        self.refresh()
        return

    def task_selected(self, event=None):
        # Enable some buttons
        self.delete_button.config(state=NORMAL)
        self.view_button.config(state=NORMAL)
        return

    def filter_by_date(self, event=None):
        date = self.cal.get_date()
        self.refresh()
        for task_name in self.unfinished_list.get_children():
            if self.tasks['tasks_list'][task_name]['date'] != date:
                self.unfinished_list.delete(task_name)
        for task_name in self.finished_list.get_children():
            if self.tasks['tasks_list'][task_name]['date'] != date:
                self.finished_list.delete(task_name)
        return

    def filter_overlapping(self, event=None):
        tag = self.time_overlap_var.get()
        self.refresh()
        if tag != 'None':
            for task_name in self.unfinished_list.get_children():
                if self.tasks['tasks_list'][task_name]['time_overlap_tag'] != tag:
                    self.unfinished_list.delete(task_name)
            for task_name in self.finished_list.get_children():
                if self.tasks['tasks_list'][task_name]['time_overlap_tag'] != tag:
                    self.finished_list.delete(task_name)
        return


# Functions
def create_todo_frame(master=None, username='', tasks_data=None):
    return _TodoFrame(master, username, tasks_data)
