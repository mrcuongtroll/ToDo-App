# Classes
class Account:

    def __init__(self, password, role='user', first_name=None, last_name=None,
                 birth_year=None, birth_month=None, birth_day=None, address=None, restriction=None):
        self.password = password
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.address = address
        self.restriction = restriction      # Format: %m/%d/%Y

    def to_dict(self):
        return self.__dict__


class Task:

    def __init__(self, username, date, start='00:00:00', end='23:59:59', location=None, note=None,
                 late=False, finish_date=None, finished=False, time_overlap_tag=None):
        self.username = username
        self.date = date
        self.start = start  # Format: %H:%M:%S
        self.end = end      # Format: %H:%M:%S
        self.location = location
        self.note = note
        self.late = late
        self.finish_date = finish_date
        self.finished = finished
        self.time_overlap_tag = time_overlap_tag

    def to_dict(self):
        return self.__dict__


# Constants:
INIT_ACCOUNTS = {'stay_signed_in': None,
                 'accounts': {'admin': Account(password='admin', role='admin').to_dict()}}
INIT_TASKS = {'time_overlap_tags': {},
              'tasks_list': {}}
