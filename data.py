# Classes
class Account:

    def __init__(self, password, role='user', first_name=None, last_name=None,
                 birth_year=None, birth_month=None, birth_day=None, address=None,
                 time_overlap_tags=(), restriction=None):
        self.password = password
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.address = address
        self.time_overlap_tags = time_overlap_tags
        self.restriction = restriction      # Format: mm/dd/YYYY

    def to_dict(self):
        return self.__dict__


class Task:

    def __init__(self, task_name, username, date, start=None, end=None, location=None, note=None,
                 status=None, finish_date=None, finished=False, time_overlap_tag=None):
        self.task_name = task_name
        self.username = username
        self.date = date
        self.start = start
        self.end = end
        self.location = location
        self.note = note
        self.status = status
        self.finish_date = finish_date
        self.finished = finished
        self.time_overlap_tag = time_overlap_tag

    def to_dict(self):
        return self.__dict__


# Constants:
INIT_ACCOUNTS = {'stay_signed_in': None,
                 'accounts': {'admin': Account(password='admin', role='admin').to_dict()}}
INIT_TASKS = {'time_overlap_tags': [],
              'tasks_list': []}
